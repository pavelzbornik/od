import csv
import os
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

from lxml.etree import iterparse

BASE_URL = (
    "https://www.szif.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2F"
    "dokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2F"
)
urls = {
    2020: BASE_URL + "1622192829773.zip",
    2019: BASE_URL + "1590753721920.zip",
    2018: BASE_URL + "1563197121858.zip",
    2017: BASE_URL + "1563197147275.zip",
}


def main(outdir: str, partial: bool = False):
    id_prijemce = 1

    with open(os.path.join(outdir, "zadatele.csv"), "w", encoding="utf8") as fz, open(
        os.path.join(outdir, "platby.csv"), "w", encoding="utf8"
    ) as fp, TemporaryDirectory() as tmpdir:
        cz = csv.DictWriter(
            fz,
            ["id_prijemce", "rok", "jmeno_nazev", "obec", "okres", "castka_bez_pvp"],
            lineterminator="\n",
        )
        cp = csv.DictWriter(
            fp,
            [
                "id_prijemce",
                "rok",
                "fond_typ_podpory",
                "opatreni",
                "zdroje_cr",
                "zdroje_eu",
                "celkem_czk",
            ],
            lineterminator="\n",
        )

        cz.writeheader()
        cp.writeheader()

        for rok_ds, url in urls.items():
            tfn = os.path.join(tmpdir, "tmp.zip")
            urlretrieve(url, tfn)

            with ZipFile(tfn) as zf:
                assert len(zf.filelist) == 1, "Vic souboru nez ocekavano: {}".format(
                    zf.filelist
                )

                with zf.open(zf.filelist[0].filename) as member:
                    et = iterparse(member)

                    rok = None
                    for num, (action, element) in enumerate(et):
                        if partial and num > 1e3:
                            break
                        assert action == "end"
                        if element.tag == "rok":
                            rok = int(element.text)
                            assert rok == rok_ds, "Necekany rok v datech"

                        if element.tag != "zadatel":
                            continue

                        zadatel = {"id_prijemce": id_prijemce, "rok": rok}

                        for key in ["jmeno_nazev", "obec", "okres", "castka_bez_pvp"]:
                            zadatel[key] = element.find(key).text

                        for elplatba in element.findall(
                            "platby/platba"
                        ) + element.findall("platby_pvp/platba_pvp"):
                            platba = {"id_prijemce": id_prijemce, "rok": rok}
                            for key in [
                                "fond_typ_podpory",
                                "opatreni",
                                "zdroje_cr",
                                "zdroje_eu",
                                "celkem_czk",
                            ]:
                                platba[key] = getattr(elplatba.find(key), "text", None)

                            cp.writerow(platba)

                        cz.writerow(zadatel)
                        id_prijemce += 1

                        element.clear()
