import urllib.parse, logging, requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from ..Movie import Movie

SITE_IDENTIFIER = "cinemathek"
SITE_NAME = "Cinemathek"


def __fetchDataFromDeeplink(url: str) -> dict:
    dRes = requests.get(str(url))
    dSoup = BeautifulSoup(dRes.text, "html.parser")
    dDescription = str((dSoup.find("div", class_="wp-content").findAll("p")[0]).text)
    dOriginalTitle = str((dSoup.findAll("span", class_="valor")[0]).text)
    return [
        dOriginalTitle,
        dDescription,
    ]


def search(title: str) -> list:
    logging.debug(f"[{SITE_NAME}]Searching for {title}")
    res = requests.get(
        "https://cinemathek.net/?s=" + str(urllib.parse.quote_plus(title.lower()))
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("div", class_="result-item")
    movieDeeplinks = list()
    movieData = list()
    movieDeeplinkData = list()
    retObj = list()
    pool = ThreadPool(processes=int(len(responseElements) + 1))
    async_result = list()
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("div", class_="title")).text)
        shortDescription = str((elemSoup.find("div", class_="contenido")).text)
        poster = elemSoup.find("div", class_="thumbnail").find("img")["src"]
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
