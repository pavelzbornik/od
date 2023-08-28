from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import (
    Boolean,
    Date,
    DateTime,
    Integer,
    Numeric,
    SmallInteger,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "etrziste_casti_vz",
        meta,
        Column("vz_systemove_cislo", Text, nullable=False),
        Column("cast_vz_cislo", SmallInteger, nullable=False),
        Column("smluvni_cena_vcetne_dph", Numeric(16, 2), nullable=True),
        Column("smluvni_cena_bez_dph", Numeric(16, 2), nullable=True),
        Column("smluvni_cena_sazba_dph", Numeric(16, 2), nullable=True),
        Column("smluvni_cena_mena", Text, nullable=True),  # TODO: enum?
    ),
    Table(
        "etrziste_polozky_vz",
        meta,
        Column("vz_systemove_cislo", Text, nullable=False),
        Column("nipez_kod", Text, nullable=True),
        Column("nipez_nazev", Text, nullable=True),
        Column("nipez_povinnost_pro_etrziste", Text, nullable=True),
        Column("nipez_nazev_vlastnosti", Text, nullable=True),
        Column("nipez_datovy_typ_vlastnosti", Text, nullable=True),
        Column("nipez_hodnota_vlastnosti", Text, nullable=True),
        Column("nipez_merna_jednotka_vlastnosti", Text, nullable=True),
        Column("nipez_operator_vlastnosti", Text, nullable=True),
    ),
    Table(
        "etrziste_kriteria_vz",
        meta,
        Column("vz_systemove_cislo", Text, nullable=False),
        Column("dilci_hodnotici_kriterium", Text, nullable=False),
        Column("dilci_hodnotici_kriterium_vaha", Numeric(5, 2), nullable=False),
        Column("dilci_kriterium_ciselne_vyjadritelne", Text, nullable=True),
        Column("dilci_kriterium_predmetem_eaukce", Text, nullable=True),
        Column(
            "dilci_kriterium_zadavatel_pozadoval_vlozeni_nabidkovych_hodnot",
            Text,
            nullable=True,
        ),
        Column("subkriterium_nabidkove_ceny", Text, nullable=True),
        Column("subkriterium_nabidkove_ceny_vaha", Numeric(5, 2), nullable=True),
        Column("subkriterium_dilciho_kriteria", Text, nullable=True),
        Column("subkriterium_dilciho_kriteria_vaha", Numeric(5, 2), nullable=True),
        Column("subkriterium_ciselne_vyjadritelne", Text, nullable=True),
        Column("subkriterium_predmetem_eaukce", Text, nullable=True),
        Column(
            "subkriterium_zadavatel_pozadoval_vlozeni_nabidkovych_hodnot",
            Text,
            nullable=True,
        ),
    ),
    Table(
        "etrziste_dodavatele",
        meta,
        Column("vz_systemove_cislo", Text, nullable=False),
        Column("cast_vz_cislo", SmallInteger, nullable=False),
        Column("datum_uzavreni_smlouvy", DateTime, nullable=True),
        Column("dodavatel_uredni_nazev", Text, nullable=False),
        Column("dodavatel_ico", Integer, nullable=True, index=True),
        Column("dodavatel_stat", Text, nullable=False),
    ),
    Table(
        "etrziste_vz",
        meta,
        Column("nazev_etrziste", Text, nullable=False),
        Column("vz_systemove_cislo", Text, nullable=False),
        Column("nazev_vz", Text, nullable=False),
        Column("vz_stav", Text, nullable=False),
        Column("vz_druh", Text, nullable=False),
        Column("vz_typ", Text, nullable=True),
        Column("druh_zadavaci_rizeni", Text, nullable=True),
        Column("predpokladana_hodnota_vz", Numeric(16, 2), nullable=False),
        Column("celkova_smluvni_cena_bez_dph", Numeric(16, 2), nullable=True),
        Column("celkova_smluvni_cena_vcetne_dph", Numeric(16, 2), nullable=True),
        Column("celkova_smluvni_cena_mena", Text, nullable=True),
        Column("zadavatel_nazev", Text, nullable=False),
        Column("zadavatel_ico", Integer, nullable=False, index=True),
        Column("zadavatel_kategorie", Text, nullable=False),
        Column("vysledek_zadavaciho_rizeni", Text, nullable=False),
        Column("datum_uzavreni_smlouvy", Date, nullable=True),
        Column("delena_na_casti", Text, nullable=False),
        Column("pocet_casti", Text, nullable=True),
        Column("pocet_polozek_vz", Text, nullable=False),
        Column("metoda_hodnoceni", Text, nullable=False),
        Column("zakladni_hodnotici_kriterium", Text, nullable=False),
        Column("zruseni_vz", Text, nullable=True),
        Column("datum_zruseni_zadavaciho_rizeni", Date, nullable=True),
        Column("byla_do_zr_zarazena_eaukce", Text, nullable=True),
        Column("pocet_vyzvanych_dodavatelu", Text, nullable=True),
        Column("pocet_obdrzenych_nabidek", Text, nullable=True),
        Column("pocet_hodnocenych_nabidek", Text, nullable=True),
        Column("namitky_pocet", Text, nullable=True),
        Column("namitky_vyhoveno", Text, nullable=True),
        Column("prezkum_ukonu", Text, nullable=True),
        Column("prezkumnych_rizeni_pocet", Text, nullable=True),
        Column("zadosti_o_dodatecne_informace_pocet", Text, nullable=True),
        Column("dodavatel_nazev", Text, nullable=True),
        Column("dodavatel_ico", Integer, nullable=True, index=True),
    ),
    Table(
        "vvz_casti_vz",
        meta,
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=True),
        Column("cislo_casti_zadani_vz", Text, nullable=True),
        Column("nazev_casti_vz", Text, nullable=True),
        Column("datum_zadani_vz", Date, nullable=True),
        Column("pocet_obdrzenych_nabidek", Integer, nullable=True),
        Column("dodavatel_nazev", Text, nullable=True),
        Column("dodavatel_ico_ze_zadani", Integer, nullable=True, index=True),
        Column("dodavatel_postovni_adresa", Text, nullable=True),
        Column("dodavatel_obec", Text, nullable=True),
        Column("dodavatel_psc", Text, nullable=True),
        Column("dodavatel_stat", Text, nullable=True),
        Column("dodavatel_www", Text, nullable=True),
        Column("puvodni_odhadovana_celkova_hodnota_vz", Numeric(16, 2), nullable=True),
        Column("puvodni_odhadovana_celkova_hodnota_vz_mena", Text, nullable=True),
        Column("puvodni_odhadovana_celkova_hodnota_vz_sazba_dph", Text, nullable=True),
        Column(
            "puvodni_odhadovana_celkova_hodnota_vz_procentni_sazba_dph",
            Numeric(4, 2),
            nullable=True,
        ),
        Column("celkova_konecna_hodnota_vz_za_zadani", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_mena_za_zadani", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_sazba_dph_za_zadani", Text, nullable=True),
        Column(
            "celkova_konecna_hodnota_vz_procentni_sazba_dph_za_zadani",
            Text,
            nullable=True,
        ),
        Column("hodnota_nejnizsi_nabidky", Numeric(16, 2), nullable=True),
        Column("hodnota_nejnizsi_nabidky_mena", Text, nullable=True),
        Column("hodnota_nejnizsi_nabidky_sazba_dph", Text, nullable=True),
        Column(
            "hodnota_nejnizsi_nabidky_procentni_sazba_dph", Numeric(4, 2), nullable=True
        ),
        Column("rocni_ci_mesicni_hodnota_pocet_roku", Integer, nullable=True),
        Column("rocni_ci_mesicni_hodnota_pocet_mesicu", Integer, nullable=True),
        Column("subdodavky_hodnota_bez_dph", Numeric(16, 2), nullable=True),
        Column("subdodavky_mena", Text, nullable=True),
        Column("subdodavky_pomer", Numeric(5, 2), nullable=True),
        Column("platny_formular", Boolean, nullable=False),
    ),
    Table(
        "vvz_vz",
        meta,
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=True),
        Column("druh_formulare", Text, nullable=False),
        Column("typ_formulare", Text, nullable=False),
        Column("vz_delena_na_casti", Text, nullable=True),
        Column("zadavatel_ico", Integer, nullable=True, index=True),
        Column("dodavatel_ico", Integer, nullable=True, index=True),
        Column("limit_vz", Text, nullable=True),
        Column("datum_odeslani_formulare_na_vvz", Date, nullable=False),
        Column("datum_uverejneni", Date, nullable=False),
        Column("zadavatel_uredni_nazev", Text, nullable=False),
        Column("zadavatel_druh", Text, nullable=True),
        Column("zadavatel_hlavni_predmet_cinnosti", Text, nullable=True),
        Column("zadavatel_zadava_jmenem_jinych", Text, nullable=True),
        Column("nazev_vz", Text, nullable=True),
        Column("druh_vz", Text, nullable=True),
        Column("kategorie_sluzeb", Text, nullable=True),
        Column("hlavni_misto_plneni", Text, nullable=True),
        Column("strucny_popis_vz", Text, nullable=True),
        Column("cpv_hlavni", Text, nullable=True),
        Column("cpv_doplnkovy1", Text, nullable=True),
        Column("cpv_doplnkovy2", Text, nullable=True),
        Column("druhy_predmet_cpv_hlavni", Text, nullable=True),
        Column("druhy_predmet_cpv_doplnkovy1", Text, nullable=True),
        Column("druhy_predmet_cpv_doplnkovy2", Text, nullable=True),
        Column("treti_predmet_cpv_hlavni", Text, nullable=True),
        Column("treti_predmet_cpv_doplnkovy1", Text, nullable=True),
        Column("treti_predmet_cpv_doplnkovy2", Text, nullable=True),
        Column("ctvrty_predmet_cpv_hlavni", Text, nullable=True),
        Column("ctvrty_predmet_cpv_doplnkovy1", Text, nullable=True),
        Column("ctvrty_predmet_cpv_doplnkovy2", Text, nullable=True),
        Column("paty_predmet_cpv_hlavni", Text, nullable=True),
        Column("paty_predmet_cpv_doplnkovy1", Text, nullable=True),
        Column("paty_predmet_cpv_doplnkovy2", Text, nullable=True),
        Column("na_vz_se_vztahuje_gpa", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_mena", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_sazba_dph", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_procentni_sazba_dph", Text, nullable=True),
        Column("nejnizsi_nabidka_vzata_vuvahu", Text, nullable=True),
        Column("nejnizsi_nabidka_vzata_vuvahu_mena", Text, nullable=True),
        Column("nejnizsi_nabidka_vzata_vuvahu_sazba_dph", Text, nullable=True),
        Column(
            "nejnizsi_nabidka_vzata_vuvahu_procentni_sazba_dph", Text, nullable=True
        ),
        Column("nejvyssi_nabidka_vzata_vuvahu", Text, nullable=True),
        Column("druh_rizeni", Text, nullable=True),
        Column("hlavni_kriteria_pro_zadani_zakazky", Text, nullable=True),
        Column("kriterium1", Text, nullable=True),
        Column("vaha_kriteria1", Text, nullable=True),
        Column("kriterium2", Text, nullable=True),
        Column("vaha_kriteria2", Text, nullable=True),
        Column("kriterium3", Text, nullable=True),
        Column("vaha_kriteria3", Text, nullable=True),
        Column("kriterium4", Text, nullable=True),
        Column("vaha_kriteria4", Text, nullable=True),
        Column("kriterium5", Text, nullable=True),
        Column("vaha_kriteria5", Text, nullable=True),
        Column("kriterium6", Text, nullable=True),
        Column("vaha_kriteria6", Text, nullable=True),
        Column("kriterium7", Text, nullable=True),
        Column("vaha_kriteria7", Text, nullable=True),
        Column("kriterium8", Text, nullable=True),
        Column("vaha_kriteria8", Text, nullable=True),
        Column("kriterium9", Text, nullable=True),
        Column("vaha_kriteria9", Text, nullable=True),
        Column("kriterium10", Text, nullable=True),
        Column("vaha_kriteria10", Text, nullable=True),
        Column("byla_pouzita_elektronicka_drazba", Text, nullable=True),
        Column("zakazka_se_vztahuje_kprojektu_fin_zes", Text, nullable=True),
        Column("projekty_ciprogramy", Text, nullable=True),
        Column("odhadovana_hodnota_vz_bez_dph", Numeric(16, 2), nullable=True),
        Column("odhadovana_hodnota_vz_mena", Text, nullable=True),
        Column("odhadovana_hodnota_vz_rozsah_od", Numeric(16, 2), nullable=True),
        Column("odhadovana_hodnota_vz_rozsah_do", Numeric(16, 2), nullable=True),
        Column("odhadovana_hodnota_vz_rozsah_mena", Text, nullable=True),
        Column("platny_formular", Boolean, nullable=False),
    ),
    Table(
        "zzvz_zadani_vz",
        meta,
        Column("id_zakazky", Text, nullable=False),
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=False),
        Column("druh_formulare", Text, nullable=False),
        Column("id_zadani", Text, nullable=False),
        Column("cislo_casti_zadani_vz", Text, nullable=True),
        Column("nazev_casti_vz", Text, nullable=True),
        Column("zadani_casti_zakazky", Text, nullable=True),
        Column("informace_o_nezadani_casti_zakazky", Text, nullable=True),
        Column("datum_zadani_vz", DateTime, nullable=True),
        Column("pocet_obdrzenych_nabidek", Text, nullable=True),
        Column("puvodni_odhadovana_celkova_hodnota_vz", Numeric(16, 2), nullable=True),
        Column("puvodni_odhadovana_celkova_hodnota_vz_mena", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz_za_zadani", Numeric(16, 2), nullable=True),
        Column("celkova_konecna_hodnota_vz_mena_za_zadani", Text, nullable=True),
        Column("hodnota_nejnizsi_nabidky", Numeric(16, 2), nullable=True),
        Column("hodnota_nejnizsi_nabidky_mena", Text, nullable=True),
        Column("hodnota_nejvyssi_nabidky", Numeric(16, 2), nullable=True),
        Column("subdodavky_hodnota_bez_dph", Numeric(16, 2), nullable=True),
        Column("subdodavky_mena", Text, nullable=True),
        Column("subdodavky_pomer", Numeric(5, 2), nullable=True),
        Column("datum_odeslani_formulare_na_vvz", DateTime, nullable=False),
        Column("platny_formular", Boolean, nullable=False),
    ),
    Table(
        "zzvz_casti_vz",
        meta,
        Column("id_zakazky", Text, nullable=False),
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=True),
        Column("druh_formulare", Text, nullable=False),
        Column("id_casti_vz", Text, nullable=False),
        Column("cislo_casti_vz", Text, nullable=True),
        Column("nazev_casti_vz", Text, nullable=True),
        Column("popis_casti_vz", Text, nullable=True),
        Column("predpokladana_celkova_hodnota_casti_vz", Numeric(16, 2), nullable=True),
        Column("predpokladana_celkova_hodnota_casti_vz_mena", Text, nullable=True),
        Column("hlavni_misto_plneni_nuts", Text, nullable=True),
        Column("hlavni_misto_plneni", Text, nullable=True),
        Column("cpv_kod", Text, nullable=True),
        Column("zakazka_se_vztahuje_kprojektu_fin_zes", Text, nullable=True),
        Column("projekty_ci_programy_fin_zes", Text, nullable=True),
        Column("datum_odeslani_formulare_na_vvz", DateTime, nullable=False),
        Column("platny_formular", Boolean, nullable=False),
    ),
    Table(
        "zzvz_dodavatele",
        meta,
        Column("id_zakazky", Text, nullable=False),
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=False),
        Column("druh_formulare", Text, nullable=False),
        Column("id_zadani", Text, nullable=False),
        Column("cislo_casti_zadani_vz", Text, nullable=True),
        Column("nazev_casti_vz", Text, nullable=True),
        Column("dodavatel_ico", Integer, nullable=True, index=True),
        Column("dodavatel_nazev", Text, nullable=False),
        Column("dodavatel_postovni_adresa", Text, nullable=True),
        Column("dodavatel_obec", Text, nullable=False),
        Column("dodavatel_psc", Text, nullable=True),
        Column("dodavatel_stat", Text, nullable=False),
        Column("dodavatel_www", Text, nullable=True),
        Column("datum_odeslani_formulare_na_vvz", DateTime, nullable=False),
        Column("platny_formular", Boolean, nullable=False),
    ),
    Table(
        "zzvz_vz",
        meta,
        Column("id_zakazky", Text, nullable=False),
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=False),
        Column("druh_formulare", Text, nullable=False),
        Column("typ_formulare", Text, nullable=False),
        Column("vz_delena_na_casti", Text, nullable=True),
        Column("zadavatel_ico", Integer, nullable=True, index=True),
        Column("limit_vz", Text, nullable=True),
        Column("datum_odeslani_formulare_na_vvz", DateTime, nullable=False),
        Column("datum_uverejneni", DateTime, nullable=False),
        Column("zadavatel_uredni_nazev", Text, nullable=False),
        Column("zadavatel_druh", Text, nullable=True),
        Column("zadavatel_hlavni_predmet_cinnosti", Text, nullable=True),
        Column("zakazka_zahrnuje_spolecne_zadavani_zakazek", Text, nullable=True),
        Column("zakazku_zadava_centralni_zadavatel", Text, nullable=True),
        Column("zadavatel_profil_url", Text, nullable=True),
        Column("zadavatel_profil_url_platnost", Text, nullable=True),
        Column("zadavatel_profil_zruseni_typ", Text, nullable=True),
        Column("zadavatel_profil_url_nova", Text, nullable=True),
        Column("datum_zruseni_ci_zneaktivneni_profilu", DateTime, nullable=True),
        Column("nazev_vz", Text, nullable=True),
        Column("druh_vz", Text, nullable=True),
        Column("strucny_popis_vz", Text, nullable=True),
        Column("cpv_hlavni", Text, nullable=True),
        Column("cpv_doplnkovy1", Text, nullable=True),
        Column("na_vz_se_vztahuje_gpa", Text, nullable=True),
        Column("celkova_konecna_hodnota_vz", Numeric(16, 2), nullable=True),
        Column("celkova_konecna_hodnota_vz_mena", Text, nullable=True),
        Column("nejnizsi_nabidka_vzata_vuvahu", Numeric(16, 2), nullable=True),
        Column("nejnizsi_nabidka_vzata_vuvahu_mena", Text, nullable=True),
        Column("nejvyssi_nabidka_vzata_vuvahu", Numeric(16, 2), nullable=True),
        Column("druh_rizeni", Text, nullable=True),
        Column("byla_pouzita_elektronicka_drazba", Text, nullable=True),
        Column("odhadovana_hodnota_vz_bez_dph", Numeric(16, 2), nullable=True),
        Column("odhadovana_hodnota_vz_mena", Text, nullable=True),
        Column("zadavatel_kontaktni_osoba", Text, nullable=True),
        Column("zadavatel_email", Text, nullable=False),
        Column("zadavatel_telefon", Text, nullable=True),
        Column("lhuta_pro_doruceni_nabidek", Text, nullable=True),
        Column("otevirani_nabidek_datum_cas", DateTime, nullable=True),
        Column("otevirani_nabidek_misto", Text, nullable=True),
        Column("otevirani_nabidek_opravnene_osoby_dalsi_info", Text, nullable=True),
        Column("uchazec_vazan_nabidkou_do", Text, nullable=True),
        Column("uchazec_vazan_nabidkou_doba_mesice", Text, nullable=True),
        Column("platny_formular", Text, nullable=False),
        Column("pravidelne_predbezne_oznameni", Text, nullable=True),
        Column("pravidelne_predbezne_oznameni_vyzva_k_soutezi", Text, nullable=True),
        Column("predbezne_oznameni", Text, nullable=True),
        Column("predbezne_oznameni_vyzva_k_soutezi", Text, nullable=True),
        Column("system_kvalifikace", Text, nullable=True),
        Column("system_kvalifikace_vyzva_k_soutezi", Text, nullable=True),
        Column("oznameni_o_zahajeni_zr", Text, nullable=True),
        Column("oznameni_o_vysledku_zr", Text, nullable=True),
        Column("oznameni_o_vysledku_ks", Text, nullable=True),
    ),
    Table(
        "zzvz_kriteria_vz",
        meta,
        Column("id_zakazky", Text, nullable=False),
        Column("id_popisu_casti_zakazky", Text, nullable=False),
        Column("evidencni_cislo_vz_na_vvz", Text, nullable=False),
        Column("cislo_formulare_na_vvz", Text, nullable=False),
        Column("druh_formulare", Text, nullable=False),
        Column("cislo_casti_vz", Text, nullable=True),
        Column("nazev_casti_vz", Text, nullable=True),
        Column("poradi_kriteria", Text, nullable=True),
        Column("kriterium_zadani_zakazky", Text, nullable=False),
        Column("nazev_kriteria", Text, nullable=True),
        Column("vaha_kriteria", Text, nullable=True),
        Column("datum_odeslani_formulare_na_vvz", DateTime, nullable=False),
        Column("platny_formular", Boolean, nullable=False),
    ),
]

# -- TODO: foreign keys? composite primary keys?

if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
