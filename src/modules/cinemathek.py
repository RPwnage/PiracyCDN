import requests
import urllib.parse
from bs4 import BeautifulSoup
from ..Movie import Movie

SITE_IDENTIFIER = "cinemathek"
SITE_NAME = "Cinemathek"


def search(title: str) -> list:
    res = requests.get(
        "https://cinemathek.net/?s=" + str(urllib.parse.quote_plus(title.lower()))
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("a", class_="poster")
    response = []
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("div", class_="title")).text)
        shortDescription = str((elemSoup.find("div", class_="contenido")).text)
        posterMaintag = elemSoup.find("div", class_="thumbnail")
        poster = posterMaintag.find("img")["src"]
        movieDeeplink = posterMaintag.find("a")["href"]

        # Fetch data from deeplink
        dRes = requests.get(str(movieDeeplink))
        dSoup = BeautifulSoup(dRes.text, "html.parser")
        dDescription = str(
            (dSoup.find("div", class_="wp-content").findAll("p")[0]).text
        )
        dOriginalTitle = str((dSoup.findAll("span", class_="valor")[0]).text)

        response.append(
            Movie(
                title, originalTitle=dOriginalTitle, poster=poster, provider=SITE_NAME
            )
        )

    return response


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
