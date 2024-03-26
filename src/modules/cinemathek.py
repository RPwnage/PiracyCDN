import urllib.parse, logging, requests, re
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from ..Movie import Movie
from ..Episode import Episode
from ..Series import Series

from ..hosters import *

HOSTERS = [vidmoly]
SITE_IDENTIFIER = "cinemathek"
SITE_NAME = "Cinemathek"


def __fetchDataFromDeeplink(url: str) -> dict:
    res = requests.get(str(url))
    mediaType = 0
    soup = BeautifulSoup(res.text, "html.parser")
    description = str((soup.find("div", class_="wp-content").findAll("p")[0]).text)
    originalTitle = str((soup.findAll("span", class_="valor")[0]).text)
    mediaId = int(soup.find("link", {"rel": "shortlink"})["href"].split("?p=")[1])
    streamLinks = list()
    streams = list()
    for index in range(50):
        resJ = requests.get(
            f"https://cinemathek.net/wp-json/dooplayer/v2/{mediaId}/movie/{index + 1}"
        ).json()
        if resJ["embed_url"] == None:
            break
        else:
            streamLinks.append(resJ["embed_url"])

    seasons = []
    if streamLinks == [] and ">Episodes<" in res.text:
        # If there is no movie data, try to get the seasons
        mediaType = 1
        seasonsSoup = soup.find("div", id="seasons")
        seasonsElem = seasonsSoup.findAll("div", class_="se-c")
        seasons = [[0]] * (len(seasonsElem))
        for index, season in enumerate(seasonsElem):
            for episode in season.findAll("li"):
                if "none" not in episode["class"]:
                    episodeTitle = str((episode.find("a")).text)
                    seasons[index].append(Episode(episodeTitle))
                    seasons[index].pop(0)

    for streamLink in streamLinks:
        for hoster in HOSTERS:
            if hoster.HOSTER_IDENTIFIER in streamLink:
                streams.append(hoster.extractStream(streamLink))

    if mediaType == 0:
        return [
            originalTitle,
            description,
            streams,
            mediaType,
        ]
    elif mediaType == 1:
        return [
            originalTitle,
            description,
            streams,
            mediaType,
        ]


def search(title: str) -> list:
    logging.info(f"[{SITE_NAME}]\tSearching for {title}")
    res = requests.get(
        "https://cinemathek.net/?s=" + str(urllib.parse.quote_plus(title.lower()))
    )
    soup = BeautifulSoup(res.text, "html.parser")
    responseElements = soup.findAll("div", class_="result-item")
    mediaDeeplinks = list()
    mediaData = list()
    mediaDeeplinkData = list()
    retObj = list()
    pool = ThreadPool(processes=int(len(responseElements) + 1))
    async_result = list()
    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("div", class_="title")).text)
        shortDescription = str((elemSoup.find("div", class_="contenido")).text)
        poster = elemSoup.find("div", class_="thumbnail").find("img")["src"]
        mediaData.append([title, shortDescription, poster])
        mediaDeeplinks.append(
            elemSoup.find("div", class_="thumbnail").find("a")["href"]
        )

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
        if mediaDeeplinkData[index][3] == 0:
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
        elif mediaDeeplinkData[index][3] == 1:
            retObj.append(
                Series(
                    title=media[0],
                    poster=media[2],
                    seasons=mediaDeeplinkData[index][2],
                )
            )

    return retObj


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
