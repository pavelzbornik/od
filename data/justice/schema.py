from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.sqltypes import (
    BigInteger,
    Boolean,
    Date,
    Numeric,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "subjekty",
        meta,
        Column("ico", BigInteger, nullable=False, primary_key=True, unique=True),
        Column("nazev", Text, nullable=False),
        Column("datum_zapis", Date, nullable=False),
        Column("datum_vymaz", Date, nullable=True),
    ),
    Table(
        "spisova_znacka",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("znacka", Text, nullable=True),
        Column("soud_kod", Text, nullable=True),
        Column("soud_nazev", Text, nullable=True),
        Column("oddil", Text, nullable=True),
        Column("vlozka", Text, nullable=True),
    ),
    Table(
        "nazev",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("nazev", Text, nullable=True),
    ),
    Table(
        "pravni_forma",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("nazev", Text, nullable=True),
        Column("zkratka", Text, nullable=True),
    ),
    Table(
        "predmet_podnikani",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("kategorie", Text, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "pocet_clenu",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("udaj_typ", Text, nullable=True),
        Column("datum_zapis", Date, nullable=True),
        Column("text", Text, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
    ),
    Table(
        "zpusob_jednani",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "ostatni_skutecnosti",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "zpusob_rizeni",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "akcie",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("podoba", Text, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("pocet", Text, nullable=True),
        Column("hodnota_typ", Text, nullable=True),
        Column("hodnota", Numeric(16, 2), nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "vklady",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("typ", Text, nullable=True),
        Column("vklad_typ", Text, nullable=True),
        Column("vklad_hodnota", Text, nullable=True),  #  -- obcas tam je pitomost
        Column("text", Text, nullable=True),
    ),
    Table(
        "pravni_duvod_vymazu",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "spolecny_text",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("udaj_typ", Text, nullable=True),
        Column("datum_zapis", Date, nullable=True),
        Column("text", Text, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
    ),
    Table(
        "exekuce",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "pravni_forma_text",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "nejvyssi_organ",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "vznik",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("datum_vznik", Date, nullable=True),
    ),
    Table(
        "majetek",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "spolecnik_zastavni_pravo",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("datum_vznik_prava", Text, nullable=True),  #  -- obcas tam je pitomost
        Column("text", Text, nullable=True),
    ),
    Table(
        "text_spravni_rada",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "spolecnik_podil",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("vklad_typ", Text, nullable=True),
        Column("vklad_hodnota", Text, nullable=True),  #  -- obcas tam je pitomost
        Column("souhrn_typ", Text, nullable=True),
        Column("souhrn_hodnota", Text, nullable=True),  #  -- obcas tam je pitomost
        Column("splaceni_typ", Text, nullable=True),
        Column("splaceni_hodnota", Text, nullable=True),  #  -- obcas tam je pitomost
        Column("druh_podilu", Text, nullable=True),
        Column("kmenovy_list", Text, nullable=True),
    ),
    Table(
        "sidlo",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("stat", Text, nullable=True),
        Column("adresa", Text, nullable=True),
        Column("obec", Text, nullable=True),
        Column("cast_obce", Text, nullable=True),
        Column("ulice", Text, nullable=True),
        Column("cislo_po", Text, nullable=True),
        Column("cislo_or", Text, nullable=True),
        Column("cislo_text", Text, nullable=True),
        Column("psc", Text, nullable=True),
        Column("okres", Text, nullable=True),
    ),
    Table(
        "konkurs_prohlaseni",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("datum_rozhodnuti", Date, nullable=True),
        Column("spisova_znacka", Text, nullable=True),
        Column("datum_vyveseni", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "konkurs_zruseni",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("hlavicka", Text, nullable=True),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "skutecny_majitel",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("specifikace", Text, nullable=True),
        Column("zakladatel", Boolean, nullable=True),
        Column("prima_ucast", Boolean, nullable=True),
        Column("valid", Boolean, nullable=True),
        Column("obmysleny", Boolean, nullable=True),
        Column("spravce", Boolean, nullable=True),
        Column("typ", Text, nullable=True),
        Column("protektor", Boolean, nullable=True),
        Column("postaveni_jinak", Boolean, nullable=True),
        Column("postaveni", Text, nullable=True),
        Column("rozdeleni_prostredku", Boolean, nullable=True),
        Column("spis_zn_sm", Text, nullable=True),
        Column("urcen_pozici_ve_stat_org", Boolean, nullable=True),
        Column("detail", Text, nullable=True),
        Column("prima_ucast_podil", Text, nullable=True),
        Column("slovni_vyjadreni", Text, nullable=True),
        Column("hlasovaci_pravo", Text, nullable=True),
        Column("disponuje", Text, nullable=True),
        Column("rozdeleni_prostredku_podil", Text, nullable=True),
        Column("email", Text, nullable=True),
        Column("podil", Text, nullable=True),
        Column("osoba_jmeno", Text, nullable=True),
        Column("osoba_prijmeni", Text, nullable=True),
        Column("osoba_datum_narozeni", Date, nullable=True),
        Column("osoba_titul_pred", Text, nullable=True),
        Column("osoba_titul_za", Text, nullable=True),
        Column("adresa_stat_nazev", Text, nullable=True),
        Column("adresa_obec", Text, nullable=True),
        Column("adresa_cast_obce", Text, nullable=True),
        Column("adresa_ulice", Text, nullable=True),
        Column("adresa_cislo_po", Text, nullable=True),
        Column("adresa_cislo_or", Text, nullable=True),
        Column("adresa_psc", Text, nullable=True),
        Column("adresa_okres", Text, nullable=True),
        Column("adresa_cislo_ev", Text, nullable=True),
        Column("adresa_text", Text, nullable=True),
        Column("bydliste_stat_nazev", Text, nullable=True),
        Column("bydliste_obec", Text, nullable=True),
        Column("bydliste_cast_obce", Text, nullable=True),
        Column("bydliste_cislo_po", Text, nullable=True),
        Column("bydliste_cislo_or", Text, nullable=True),
        Column("bydliste_psc", Text, nullable=True),
        Column("bydliste_ulice", Text, nullable=True),
    ),
    Table(
        "skutecny_majitel_primy",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("clenstvi_od", Date, nullable=True),
        Column("clenstvi_do", Date, nullable=True),
        Column("spravce", Boolean, nullable=True),
        Column("typ", Text, nullable=True),
        Column("postaveni", Text, nullable=True),
        Column("podil_na_prospechu_typ", Text, nullable=True),
        Column("podil_na_prospechu_hodnota", Text, nullable=True),
        Column("podil_na_hlasovani_typ", Text, nullable=True),
        Column("podil_na_hlasovani_hodnota", Text, nullable=True),
        Column("vlastni_podil_na_hlasovani", Boolean, nullable=True),
        Column("vlastni_podil_na_prospechu", Boolean, nullable=True),
        Column("znepristupneni", Boolean, nullable=True),
        Column("uverejneni", Boolean, nullable=True),
        Column("jina_skutecnost_prijemce", Boolean, nullable=True),
        Column("osoba_jmeno", Text, nullable=True),
        Column("osoba_prijmeni", Text, nullable=True),
        Column("osoba_datum_narozeni", Text, nullable=True),
        Column("osoba_titul_pred", Text, nullable=True),
        Column("osoba_titul_za", Text, nullable=True),
        Column("adresa_stat_nazev", Text, nullable=True),
        Column("adresa_obec", Text, nullable=True),
        Column("adresa_cast_obce", Text, nullable=True),
        Column("adresa_ulice", Text, nullable=True),
        Column("adresa_cislo_po", Text, nullable=True),
        Column("adresa_cislo_or", Text, nullable=True),
        Column("adresa_psc", Text, nullable=True),
        Column("adresa_okres", Text, nullable=True),
        Column("adresa_cislo_ev", Text, nullable=True),
        Column("adresa_text", Text, nullable=True),
        Column("bydliste_stat_nazev", Text, nullable=True),
        Column("bydliste_obec", Text, nullable=True),
        Column("bydliste_cast_obce", Text, nullable=True),
        Column("bydliste_cislo_po", Text, nullable=True),
        Column("bydliste_cislo_or", Text, nullable=True),
        Column("bydliste_psc", Text, nullable=True),
        Column("bydliste_ulice", Text, nullable=True),
    ),
    Table(
        "insolvencni_zapis",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("id", Text, nullable=True),
        Column("aktivni", Text, nullable=True),
        Column("key", Text, nullable=True),
        Column("nazev", Text, nullable=True),
        Column("ciselnik", Text, nullable=True),
        Column("externi_kod", Text, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "vyrovnani",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("text", Text, nullable=True),
    ),
    Table(
        "angazovane_osoby",
        meta,
        Column("ico", ForeignKey("subjekty.ico")),
        Column("datum_zapis", Date, nullable=True),
        Column("datum_vymaz", Date, nullable=True),
        Column("udaj_typ", Text, nullable=True),
        Column("funkce", Text, nullable=True),
        Column("funkce_od", Date, nullable=True),
        Column("clenstvi_od", Date, nullable=True),
        Column("clenstvi_do", Date, nullable=True),
        Column("funkce_do", Date, nullable=True),
        Column("jmeno", Text, nullable=True),
        Column("prijmeni", Text, nullable=True),
        Column("titul_pred", Text, nullable=True),
        Column("titul_za", Text, nullable=True),
        Column("datum_narozeni", Date, nullable=True),
        Column("nazev", Text, nullable=True),
        Column("reg_cislo", Text, nullable=True),
        Column("ico_angos", BigInteger, nullable=True),
        Column("euid", Text, nullable=True),
        Column("adresa_stat", Text, nullable=True),
        Column("adresa_obec", Text, nullable=True),
        Column("adresa_cast_obce", Text, nullable=True),
        Column("adresa_ulice", Text, nullable=True),
        Column("adresa_cislo_po", Text, nullable=True),
        Column("adresa_psc", Text, nullable=True),
        Column("adresa_okres", Text, nullable=True),
        Column("adresa_cislo_or", Text, nullable=True),
        Column("adresa_adresa_text", Text, nullable=True),
        Column("adresa_cislo_ev", Text, nullable=True),
        Column("adresa_doplnujici_text", Text, nullable=True),
        Column("adresa_cislo_text", Text, nullable=True),
        Column("bydliste_stat", Text, nullable=True),
        Column("bydliste_ulice", Text, nullable=True),
        Column("bydliste_obec", Text, nullable=True),
        Column("bydliste_psc", Text, nullable=True),
        Column("bydliste_cast_obce", Text, nullable=True),
        Column("bydliste_cislo_po", Text, nullable=True),
        Column("bydliste_cislo_or", Text, nullable=True),
        Column("bydliste_okres", Text, nullable=True),
        Column("bydliste_cislo_ev", Text, nullable=True),
        Column("bydliste_cislo_text", Text, nullable=True),
        Column("bydliste_doplnujici_text", Text, nullable=True),
    ),
]


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
