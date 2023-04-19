# download csv file with urllib
import os
from urllib.request import urlretrieve

URL_DICT = {
    "CEA-programy.csv": "https://www.isvavai.cz/dokumenty/open-data/CEA-programy.csv",
    "CEA-poskytovatel.csv": "https://www.isvavai.cz/dokumenty/open-data/CEA-poskytovatel.csv",
    "CEA-prijemce.csv": "https://www.isvavai.cz/dokumenty/open-data/CEA-prijemce.csv",
    "VES.csv": "https://www.isvavai.cz/dokumenty/open-data/VES.csv",
    "CEP-projekty.csv": "https://www.isvavai.cz/dokumenty/open-data/CEP-projekty.csv",
    "CEP-ucastnici.csv": "https://www.isvavai.cz/dokumenty/open-data/CEP-ucastnici.csv",
    "RIV-2018.csv": "https://www.isvavai.cz/dokumenty/open-data/RIV-2018.csv",
    "RIV-2019.csv": "https://www.isvavai.cz/dokumenty/open-data/RIV-2019.csv",
    "RIV-2020.csv": "https://www.isvavai.cz/dokumenty/open-data/RIV-2020.csv",
    "RIV-2021.csv": "https://www.isvavai.cz/dokumenty/open-data/RIV-2021.csv",
}


def main(outdir: str, partial: bool = False):
    for fn, url in URL_DICT.items():
        print(f"Stahuji {fn} z {url}")
        ofn = os.path.join(outdir, fn)
        urlretrieve(url, ofn)


if __name__ == "__main__":
    main(".")
