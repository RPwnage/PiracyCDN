import requests, logging
from ..Movie import Movie
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

from ..hosters import *

HOSTERS = [voe, doodstream, gxplayer]
SITE_IDENTIFIER = "megakino"
SITE_NAME = "Megakino"


def __fetchDataFromDeeplink(url: str) -> dict:
    res = requests.get(str(url))
    soup = BeautifulSoup(res.text, "html.parser")
    description = str((soup.find("div", class_="page__text")).text)
    if soup.find("span", itemprop="dateCreated") is not None:
        dateCreated = str((soup.find("span", itemprop="dateCreated")).text)
    originalTitle = str((soup.find("div", class_="pmovie__original-title")).text)[1:]
    mediaType = str((soup.find("div", class_="pmovie__genres")).text).split(" ")[0]
    streams = list()
    hosters = soup.findAll("iframe")

    # Check if the media type is a Movie
    if "Serien" not in mediaType:
        for dHoster in hosters:
            if dHoster.has_attr("data-src"):
                # Exclude Youtube videos
                if "youtube" not in dHoster["data-src"]:
                    # Pick the hoster for the given stream
                    for hoster in HOSTERS:
                        if hoster.HOSTER_IDENTIFIER in dHoster["data-src"]:
                            streams.append(hoster.extractStream(dHoster["data-src"]))

    return [originalTitle, description, streams]


def search(title: str) -> list:
    logging.info(f"[{SITE_NAME}]\tSearching for {title}")
    res = requests.get(
        "https://megakino.co/index.php?do=search&subaction=search&story="
        + title.lower()
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("a", class_="poster")
    mediaDeeplinks = list()
    mediaData = list()
    mediaDeeplinkData = list()
    retObj = list()
    pool = ThreadPool(processes=int(len(responseElements) + 1))
    async_result = list()
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("h3", class_="poster__title")).text)
        shortDescription = str((elemSoup.find("div", class_="poster__text")).text)
        poster = str("https://megakino.co/" + (elemSoup.find("img"))["data-src"])
        mediaData.append([title, shortDescription, poster])
        mediaDeeplinks.append(elemSoup.find("a", class_="poster")["href"])

    for mediaDeeplink in mediaDeeplinks:
        logging.info(
            f"[{SITE_NAME}]\tAdding Thread for Deeplink request ({mediaDeeplink})"
        )
        async_result.append(
            pool.apply_async(__fetchDataFromDeeplink, (str(mediaDeeplink),))
        )

    for index, result in enumerate(async_result):
        mediaDeeplinkData.append(result.get())

    for index, media in enumerate(mediaData):
        retObj.append(
            Movie(
                title=media[0],
                originalTitle=mediaDeeplinkData[index][0],
                shortDescription=media[1],
                description=mediaDeeplinkData[index][1],
                poster=media[2],
                provider=SITE_NAME,
                streams=mediaDeeplinkData[index][2],
            )
        )

    return retObj


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
