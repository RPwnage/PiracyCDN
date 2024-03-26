import requests
from ..Movie import Movie
from bs4 import BeautifulSoup

SITE_IDENTIFIER = "megakino"
SITE_NAME = "Megakino"


def fetchDataFromDeeplink(url: str) -> dict:
    pass


def search(title: str) -> list:
    res = requests.get(
        "https://megakino.co/index.php?do=search&subaction=search&story="
        + title.lower()
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("a", class_="poster")
    response = []
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("h3", class_="poster__title")).text)
        shortDescription = str((elemSoup.find("div", class_="poster__text")).text)
        poster = str("https://megakino.co/" + (elemSoup.find("img"))["data-src"])
        movieDeeplink = (elemSoup.find("a", class_="poster"))["href"]

        # Fetch data from deeplink
        dRes = requests.get(str(movieDeeplink))
        dSoup = BeautifulSoup(dRes.text, "html.parser")
        dDescription = str((dSoup.find("div", class_="page__text")).text)
        if dSoup.find("span", itemprop="dateCreated") is not None:
            dDateCreated = str((dSoup.find("span", itemprop="dateCreated")).text)
        dCountryOfOrigin = str((dSoup.find("span", itemprop="countryOfOrigin")).text)
        dRecommendedAge = str((dSoup.find("div", class_="pmovie__age")).text)
        dOriginalTitle = str((dSoup.find("div", class_="pmovie__original-title")).text)[
            1:
        ]
        dMediaType = str((dSoup.find("div", class_="pmovie__genres")).text).split(" ")[
            0
        ]
        if "Serien" in dMediaType:
            dMediaType = "series"
        else:
            dMediaType = "movies"

        response.append(
            Movie(
                title,
                originalTitle=dOriginalTitle,
                shortDescription=shortDescription,
                description=dDescription,
                poster=poster,
                provider=SITE_NAME,
            )
        )

    return response


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
