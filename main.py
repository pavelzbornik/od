import argparse
import csv
import os
import shutil
import tempfile
import time
import warnings
from collections import defaultdict
from importlib import import_module

from sqlalchemy import Boolean, MetaData, Table, create_engine, text
from sqlalchemy.schema import AddConstraint, DropConstraint, ForeignKeyConstraint


def warninger(message, category, filename, lineno, line=None):
    return f"{filename}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = warninger

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connstring", type=str, help="connection string pro databazi tve volby"
    )
    parser.add_argument(
        "--schema_prefix",
        type=str,
        default="",
        help="prefix pro nazvy schemat (postgres) ci tabulek (sqlite)",
    )
    parser.add_argument(
        "--drop-first",
        action="store_true",
        help="před importem smaz tabulky (dobre pri zmene schematu)",
    )
    parser.add_argument(
        "--load-only",
        action="store_true",
        help="nestahuj data, jen nahraj existující CSV do databáze",
    )
    parser.add_argument(
        "--partial",
        action="store_true",
        help="procesuj jen cast vstupnich dat - vhodne pro testovani, CI apod.",
    )
    parser.add_argument("--all", action="store_true", help="procesuj vsechny moduly")
    parser.add_argument("modules", nargs="*", help="specify which datasets to include")
    args = parser.parse_args()

    if args.all and len(args.modules) > 0:
        raise ValueError("specifikuj bud --all, nebo specificke datasety, ne oboji")

    if args.load_only and not args.connstring:
        raise ValueError("při --load-only je třeba specifikovat --connstring")

    base_outdir = "csv"
    os.makedirs(base_outdir, exist_ok=True)

    engine = None
    if args.connstring:
        engine = create_engine(args.connstring)

    # TODO: nejak pridat `czechinvest` - je to ready, jen nefunguje stahovani souboru
    module_names = [
        "red",
        # TODO: docasne vypnuto, protoze jsem zkracoval nazvy tabulek, ktery
        # ted nesedej mezi schematem a mappingem
        # "cssz",
        "datovky",
        "dotinfo",
        "eufondy",
        "iissp",
        "czechpoint",
        "justice",
        "psp",
        "steno",
        "smlouvy",
        "szif",
        "zakazky",
        "volby",
        "udhpsh",
        "res",
        "ruian",
        "ares",  # schvalne na konci, protoze nacita hodne dat
    ]
    if args.modules:
        module_names = args.modules
    modules = {}
    schemas = {}

    for module in module_names:
        modules[module] = import_module(f"data.{module}.main").main
        schemas[module] = import_module(f"data.{module}.schema").schema

    # TODO: multiprocessing
    for module_name, module in modules.items():
        print(module_name)
        print("=" * len(module_name))

        outdir = os.path.join(base_outdir, module_name)
        with tempfile.TemporaryDirectory(dir=base_outdir) as outdir_tmp:
            if os.path.isdir(outdir) and not args.load_only:
                shutil.rmtree(outdir)

            if not args.load_only:
                module(outdir_tmp, partial=args.partial)
                os.rename(outdir_tmp, outdir)

        if not engine:
            continue

        table_loads = defaultdict(list)
        for table in schemas[module_name]:
            fn_cand = os.path.join(outdir, table.name + ".csv")
            dir_cand = os.path.join(outdir, table.name)
            if os.path.isfile(fn_cand):
                table_loads[(module_name, table.name)].append(fn_cand)
            elif os.path.isdir(dir_cand):
                for basename in os.listdir(dir_cand):
                    table_loads[(module_name, table.name)].append(
                        os.path.join(dir_cand, basename)
                    )
            else:
                raise IOError(f"neexistujou data pro {module_name}.{table.name}")

        for table in schemas[module_name]:
            t = time.time()
            print(f"Nahravam {table.name} do {module_name}", end="")
            files = table_loads[(module_name, table.name)]
            fkeys = [
                j for j in table.constraints if isinstance(j, ForeignKeyConstraint)
            ]

            # základní kontrola integrity (oflagovat?)
            # .lower() na obou stranach pro case insensitive porovnani
            db_column_names = [j.name.lower() for j in table.columns]
            db_column_nullable = [j.nullable for j in table.columns]
            data_nullable = [False for _ in table.columns]
            for file in files:
                with open(file, "rt", encoding="utf-8") as f:
                    cr = csv.reader(f)
                    header = [j.lower() for j in next(cr)]
                    if header != db_column_names:
                        errmap = dict(
                            (k, v) for k, v in zip(header, db_column_names) if k != v
                        )
                        warnings.warn(f"databáze očekává jiné sloupce: {errmap}")

                    for j, row in enumerate(cr):
                        if len(row) != len(db_column_names):
                            raise ValueError(
                                f"nečekaný počet sloupců, {len(row)} vs."
                                f" {len(db_column_names)} (řádka {j+2}"
                            )
                        for k, val in enumerate(row):
                            if val == "":
                                data_nullable[k] = True

            if data_nullable != db_column_nullable:
                for j, (dnull, dbnull) in enumerate(
                    zip(data_nullable, db_column_nullable)
                ):
                    if dnull == dbnull:
                        continue
                    warnings.warn(
                        f"NULL neshoda v {table.name} ({db_column_names[j]}):"
                        f" data ({dnull}) vs. DB ({dbnull})"
                    )

            if engine.name == "postgresql":
                table.schema = f"{args.schema_prefix}{module_name}"
                with engine.begin() as conn:
                    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {table.schema}"))
            elif engine.name == "sqlite":
                table.name = f"{args.schema_prefix}{module_name}_{table.name}"

            if args.drop_first:
                table.drop(engine, checkfirst=True)
            table.create(engine, checkfirst=True)

            # dropni fkeys pred nahravanim dat
            # z nejakeho duvodu jsou v sqlite nepojmenovany klice
            if engine.name == "postgresql":
                dbtable = Table(
                    table.name,
                    MetaData(engine),
                    schema=table.schema,
                    autoload_with=engine,
                )
                for fk in dbtable.constraints:
                    if isinstance(fk, ForeignKeyConstraint):
                        sql = DropConstraint(fk).compile()
                        with engine.begin() as conn:
                            conn.execute(text(sql.string))

            if engine.name == "postgresql":
                full_table_name = f"{table.schema}.{table.name}"
                conn = engine.raw_connection()
                cur = conn.cursor()
                cur.execute(f"TRUNCATE {full_table_name} CASCADE")  # TODO: cascade yolo
                for filename in files:
                    with open(filename, "rt", encoding="utf-8") as f:
                        cur.copy_expert(
                            f"COPY {full_table_name} FROM stdin WITH CSV HEADER", f
                        )
                conn.commit()  # TODO: proc nejde context manager? starej psycopg?
            elif engine.name == "sqlite":
                conn = engine.raw_connection()
                conn.execute(f"DELETE FROM {table.name}")  # truncate v sqlite neni

                ph = ", ".join(["?"] * len(table.columns))
                query = f"INSERT INTO {table.name} VALUES({ph})"
                bools = [isinstance(j.type, Boolean) for j in table.columns]
                for filename in files:
                    buffer = []
                    with open(filename, "rt", encoding="utf-8") as f:
                        cr = csv.reader(f)
                        next(cr)  # header
                        for row in cr:
                            row = [
                                bool(el) if bools[j] and el != "" else el
                                for j, el in enumerate(row)
                            ]
                            row = [None if j == "" else j for j in row]
                            buffer.append(row)
                            if len(buffer) == 100:
                                conn.executemany(query, buffer)
                                buffer = []
                        if len(buffer) > 0:
                            conn.executemany(query, buffer)
                conn.commit()
            else:
                raise IOError(f"{engine.name} not supported yet")

            # constrainty jsme neumeli dropnout u sqlite... a nejdou ani pridat
            if engine.name == "postgresql":
                for fk in fkeys:
                    if not isinstance(fk, ForeignKeyConstraint):
                        continue
                    sql = AddConstraint(fk).compile()
                    with engine.begin() as conn:
                        conn.execute(text(sql.string))

            print(f" ({time.time() - t:.2f}s)")
