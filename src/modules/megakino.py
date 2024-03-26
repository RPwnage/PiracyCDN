import requests
from ..Movie import Movie
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool


SITE_IDENTIFIER = "megakino"
SITE_NAME = "Megakino"


def __fetchDataFromDeeplink(url: str) -> dict:
    dRes = requests.get(str(url))
    dSoup = BeautifulSoup(dRes.text, "html.parser")
    dDescription = str((dSoup.find("div", class_="page__text")).text)
    if dSoup.find("span", itemprop="dateCreated") is not None:
        dDateCreated = str((dSoup.find("span", itemprop="dateCreated")).text)
    dOriginalTitle = str((dSoup.find("div", class_="pmovie__original-title")).text)[1:]

    return [dOriginalTitle, dDescription]


def search(title: str) -> list:
    res = requests.get(
        "https://megakino.co/index.php?do=search&subaction=search&story="
        + title.lower()
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("a", class_="poster")
    movieDeeplinks = list()
    movieData = list()
    movieDeeplinkData = list()
    retObj = list()
    pool = ThreadPool(processes=int(len(responseElements) + 1))
    async_result = list()
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("h3", class_="poster__title")).text)
        shortDescription = str((elemSoup.find("div", class_="poster__text")).text)
        poster = str("https://megakino.co/" + (elemSoup.find("img"))["data-src"])
        movieData.append([title, shortDescription, poster])
        movieDeeplinks.append(
            elemSoup.find("div", class_="thumbnail").find("a")["href"]
        )

    for movieDeeplink in movieDeeplinks:
        async_result.append(
            pool.apply_async(__fetchDataFromDeeplink, (str(movieDeeplink),))
        )

    for index, result in enumerate(async_result):
        movieDeeplinkData.append(result.get())

    for index, movie in enumerate(movieData):
        retObj.append(
            Movie(
                title=movie[0],
                originalTitle=movieDeeplinkData[index][0],
                shortDescription=movie[1],
                description=movieDeeplinkData[index][1],
                poster=movie[2],
                provider=SITE_NAME,
            )
        )

    return retObj


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
