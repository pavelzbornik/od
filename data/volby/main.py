import csv
import functools
import json
import multiprocessing
import os
import shutil
import zipfile
from collections import defaultdict
from contextlib import contextmanager
from fnmatch import fnmatch
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

import lxml.etree

RETRIES = 5
DVOUKOLAK = ("senat", "prezident")


@contextmanager
def load_remote_data(url: str):
    with TemporaryDirectory() as tmpdir:
        fn = os.path.basename(url)
        tfn = os.path.join(tmpdir, fn)
        if not os.path.isfile(tfn):
            req = Request(url, headers={"User-Agent": "https://github.com/kokes/od"})
            for j in range(RETRIES):
                try:
                    with urlopen(req, timeout=15) as r, open(tfn, "wb") as fw:
                        shutil.copyfileobj(r, fw)
                        break
                except URLError as e:
                    if j == RETRIES - 1:
                        raise e
                    print(f"URLError ({e}), retrying {url}")
                    continue

        with zipfile.ZipFile(tfn) as zf:
            yield zf


def extract_elements(zf, fn, nodename):
    if not fn.lower().endswith(".xml"):
        raise NotImplementedError(fn)

    with zf.open(fn) as f:
        et = lxml.etree.iterparse(f)

        for _, node in et:
            if not node.tag.endswith(f"}}{nodename}"):
                continue

            yield dict(
                (j.tag[j.tag.rindex("}") + 1 :], j.text) for j in node.iterchildren()
            )
            node.clear()


def process_url(outdir, partial, fnmap, url: str, volby: str, datum: str):
    # specialni handling davkovych exportu (nejsou v zipu)
    if not url.endswith(".zip"):
        ds, fmp = fnmap[volby]["davky.xml"]  # 'davky.xml' je dummy hodnota
        tfn = os.path.join(outdir, f"{volby}_davky.csv")
        with open(tfn, "wt", encoding="utf8") as fw:
            schema = ["DATUM"] + [j for j in fmp["schema"]]
            if volby in DVOUKOLAK:
                schema.insert(1, "KOLO")
            cw = csv.DictWriter(
                fw,
                fieldnames=schema,
                lineterminator="\n",
            )
            cw.writeheader()

            parsed = urlparse(url)
            qs = dict(parse_qsl(parsed.query))
            for kolo in [1, 2]:
                for davka in range(1, 1000):
                    if volby in DVOUKOLAK:
                        qs["kolo"] = kolo
                    elif kolo == 2:
                        break
                    qs["davka"] = davka
                    parsed = parsed._replace(query=urlencode(qs))
                    with urlopen(urlunparse(parsed)) as r:
                        et = lxml.etree.parse(r).getroot()
                    ns = et.nsmap[None]
                    if et.find(f"./{{{ns}}}CHYBA") is not None:
                        break

                    okrsky = et.findall(f"./{{{ns}}}OKRSEK")
                    # assert len(okrsky) > 0
                    for okrsek in okrsky:
                        ks = okrsek.attrib.keys()
                        assert set(ks) == set(fmp["schema"]), (volby, ks)
                        row = dict(okrsek.attrib)
                        row["DATUM"] = datum
                        if volby in DVOUKOLAK:
                            row["KOLO"] = kolo
                        cw.writerow(row)
        return

    # bezny prubeh extrakce ze zipu
    with load_remote_data(url) as zf:
        for ff in map(lambda x: x.filename, zf.filelist):
            patterns = [j for j in fnmap[volby].keys() if fnmatch(ff, j)]
            if len(patterns) == 0:
                continue
            if len(patterns) > 1:
                raise KeyError("ambiguous keys: {}".format(patterns))

            ds, fmp = fnmap[volby].get(patterns[0])
            tdir = os.path.join(outdir, f"{volby}_{ds}")
            os.makedirs(tdir, exist_ok=True)
            url_path = os.path.splitext(os.path.basename(urlparse(url).path))[0]
            tfn = os.path.join(
                tdir, f"{datum}_{url_path}_{os.path.splitext(ff)[0]}.csv"
            )
            if os.path.isfile(tfn):
                raise IOError(f"necekany prepis souboru: {tfn}")
            with open(tfn, "wt", encoding="utf8") as fw:
                cw = csv.DictWriter(
                    fw,
                    fieldnames=["DATUM"] + fmp["schema"] + fmp.get("extra_schema", []),
                    lineterminator="\n",
                )
                cw.writeheader()
                for ne, el in enumerate(extract_elements(zf, ff, fmp["klic"])):
                    if partial and ne > 1e4:
                        break
                    for k in fmp.get("vynechej", []):
                        el.pop(k, None)

                    # TODO: TEST: HLASY_01 vs. HLASY_K1
                    hk = [
                        k
                        for k in el.keys()
                        if k.startswith("HLASY_") and k.partition("_")[-1].isdigit()
                    ]
                    if hk:
                        hlasy = []
                        for k in hk:
                            hlasy.append(el[k] or 0)
                            del el[k]

                        # pg array representation - '{a, b, c}'
                        el["HLASY"] = "{{{}}}".format(",".join(map(str, hlasy)))

                    # mandat str -> bool
                    if "MANDAT" in el and el["MANDAT"] not in ("", None):
                        assert el["MANDAT"] in ("A", "1", "N", "0", 1, 0), el["MANDAT"]
                        el["MANDAT"] = (
                            "true" if el["MANDAT"] in ("A", "1", 1) else "false"
                        )

                    # u nekterych voleb je uvedeno, ke kteremu dni plati, protoze
                    # treba soud rozhodl o nejake zmene - tak pak muze byt datum
                    # uvedeno dvakrat
                    # 20181223 -> 2018-12-23
                    if "DATUMVOLEB" in el:
                        dv = el["DATUMVOLEB"]
                        assert dv.isdigit(), dv
                        assert len(dv) == 8, dv
                        el["DATUMVOLEB"] = f"{dv[:4]}-{dv[4:6]}-{dv[6:8]}"

                    cw.writerow(
                        {
                            "DATUM": datum,
                            **el,
                        }
                    )


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        mps = json.load(f)

    ncpu = multiprocessing.cpu_count()
    jobs = []
    fnmap = defaultdict(dict)
    for volby, mp in mps.items():
        for ds, spec in mp["ds"].items():
            for fn in spec["fn"]:
                assert fn not in fnmap, fn
                fnmap[volby][fn] = (ds, spec)

        for datum, urls in mp["url"].items():
            if partial and datum != sorted(mp["url"].keys())[-1]:
                continue
            for url in urls:
                jobs.append((url, volby, datum))

    job_processor = functools.partial(process_url, outdir, partial, fnmap)
    with multiprocessing.Pool(ncpu) as pool:
        pool.starmap(job_processor, jobs)


if __name__ == "__main__":
    main(".")
