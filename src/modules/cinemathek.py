import urllib.parse, logging, requests, re
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool, ApplyResult
from ..Movie import Movie
from ..Episode import Episode
from ..Series import Series

from ..hosters import *

HOSTERS = [vidmoly]
SITE_IDENTIFIER = "cinemathek"
SITE_NAME = "Cinemathek"


def __fetchDataFromEpisode(url: str) -> dict:
    logging.info(f"Fetching episode data from {url}")
    res = requests.get(str(url))
    soup = BeautifulSoup(res.text, "html.parser")
    description = str((soup.find("div", class_="wp-content")).find("p").text)
    title = str((soup.find("h3", class_="epih3")).text)
    return {"description": description, "title": title}


def __fetchDataFromDeeplink(url: str) -> dict:
    mediaType = 0
    res = requests.get(str(url))
    soup = BeautifulSoup(res.text, "html.parser")
    description = str((soup.find("div", class_="wp-content").findAll("p")[0]).text)
    originalTitle = str((soup.findAll("span", class_="valor")[0]).text)
    mediaId = int(soup.find("link", {"rel": "shortlink"})["href"].split("?p=")[1])
    pool = ThreadPool()
    async_result = list()
    streamLinks = list()
    streams = list()
    seasons = list()
    for index in range(50):
        resJ = requests.get(
            f"https://cinemathek.net/wp-json/dooplayer/v2/{mediaId}/movie/{index + 1}"
        ).json()
        if resJ["embed_url"] == None:
            break
        else:
            streamLinks.append(resJ["embed_url"])

    if streamLinks == [] and ">Episodes<" in res.text:
        # If there is no movie data, try to get the seasons
        mediaType = 1
        seasonsSoup = soup.find("div", id="seasons")
        seasonsElem = seasonsSoup.findAll("div", class_="se-c")
        episodeResults = [[0]] * (len(seasonsElem))
        seasons = [[0]] * (len(seasonsElem))
        for index, season in enumerate(seasonsElem):
            for episode in season.findAll("li"):
                if "none" not in episode["class"]:
                    episodeTitle = str((episode.find("a")).text)
                    if episodeResults[index][0] == 0:
                        episodeResults[index].pop(0)
                    # Append a pseudo element to the end of the list to indicate that there are n amount of episodes
                    seasons[index].append(1)
                    if seasons[index][0] == 0:
                        seasons[index].pop(0)
                    episodeResults[index].append(
                        pool.apply_async(
                            __fetchDataFromEpisode, (str((episode.find("a")["href"])),)
                        )
                    )

        for indexO, season in enumerate(seasons):
            for index, results in enumerate(episodeResults[indexO]):
                if type(results) == ApplyResult:
                    episodeResults[indexO][index] = results.get()
                if type(results) != ApplyResult and type(results) != Episode:
                    episodeResults[indexO][index] = Episode(
                        episodeResults[indexO][index]["title"],
                        episodeResults[indexO][index]["description"],
                    )

        for indexO, season in enumerate(seasons):
            for index, episode in enumerate(episodeResults[indexO]):
                seasons[indexO][index] = episode

    if streamLinks != [] and ">Episodes<" not in res.text:
        # If there is movie data, just get the streams
        for streamLink in streamLinks:
            for hoster in HOSTERS:
                if hoster.HOSTER_IDENTIFIER in streamLink:
                    async_result.append(
                        pool.apply_async(hoster.extractStream, (str(streamLink),))
                    )

        for result in async_result:
            streams.append(result.get())

    if mediaType == 0:
        return {
            "originalTitle": originalTitle,
            "description": description,
            "streams": streams,
            "mediaType": mediaType,
        }

    return {
        "originalTitle": originalTitle,
        "description": description,
        "seasons": seasons,
        "mediaType": mediaType,
    }


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
        if mediaDeeplinkData[index]["mediaType"] == 0:
            retObj.append(
                Movie(
                    title=media[0],
                    originalTitle=mediaDeeplinkData[index]["originalTitle"],
                    shortDescription=media[1],
                    description=mediaDeeplinkData[index]["description"],
                    poster=media[2],
                    provider=SITE_NAME,
                    streams=mediaDeeplinkData[index]["streams"],
                )
            )
        elif mediaDeeplinkData[index]["mediaType"] == 1:
            retObj.append(
                Series(
                    title=media[0],
                    poster=media[2],
                    seasons=mediaDeeplinkData[index]["seasons"],
                )
            )

    return retObj


def showEpisodes(titleId: int) -> list:
    pass


def showSeasons(titleId: int) -> list:
    pass
