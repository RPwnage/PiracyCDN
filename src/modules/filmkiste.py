import requests, logging, re
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from ..Movie import Movie

from ..hosters import *

HOSTERS = [vidmoly, voe, doodstream, gxplayer, vidmoly]
SITE_IDENTIFIER = "filmkiste"
SITE_NAME = "Filmkiste"


def __fetchDataFromEpisode(url: str) -> dict:
    pass


def __fetchDataFromDeeplink(url: str) -> dict:
    mediaType = int()
    res = requests.get(str(url))
    soup = BeautifulSoup(res.text, "html.parser")
    tvApiKey = re.search(r"tvapikey\":\"(.*?)\"", str(res.text))
    streamLinks = list()
    if tvApiKey != None:
        # This is a tv show
        mediaType = 1
        tvApiKey = tvApiKey.group(1)
        tvId = re.search(r"tvid\":\"(.*?)\"", str(res.text))
        tvApires = requests.get(
            f"https://api.themoviedb.org/3/tv/{tvId}/season/1?api_key={tvApiKey}&language=en-ENinclude_image_language=en,null"
        )

    else:
        # This is a movie
        mediaType = 0
        streams = list()
        async_result = list()
        pool = ThreadPool()
        description = str((soup.find("div", class_="desc")).text)

        # TODO: find the real original Title. This is the displayed title, and only a placeholder for now
        originalTitle = str((soup.find("h1", class_="title")).text)
        streamLinks.append(
            re.search(
                r"loadEmbed\(\'(.*?)\'\);",
                str(res.text),
            ).group(1)
        )

        if len(streamLinks) != 0:
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


def search(title: str) -> list:
    logging.info(f"[{SITE_NAME}]\tSearching for {title}")
    responseElements = list()
    mediaDeepLinks = list()
    mediaDeeplinkData = list()
    mediaData = list()
    retObj = list()
    async_result = list()
    pool = ThreadPool()

    for siteNumber in range(1, 100):
        res = requests.get(f"https://filmkiste.to/page/{siteNumber}/?s={title}")
        if res.status_code != 200:
            break
        soup = BeautifulSoup(res.text, "html.parser")
        responseElements.extend(soup.findAll("div", class_="format-standard"))

    for responseElement in responseElements:
        elemSoup = BeautifulSoup(str(responseElement), "html.parser")
        title = str((elemSoup.find("div", class_="title")).text)
        shortDescription = str((elemSoup.find("div", class_="desc")).text)
        poster = str((elemSoup.find("img"))["data-src"])
        mediaData.append([title, shortDescription, poster])
        mediaDeepLinks.append(elemSoup.find("a", class_="title")["href"])

    for mediaDeeplink in mediaDeepLinks:
        logging.info(
            f"[{SITE_NAME}]\tAdding Thread for Deeplink request ({mediaDeeplink})"
        )
        async_result.append(
            pool.apply_async(__fetchDataFromDeeplink, (str(mediaDeeplink),))
        )

    for result in async_result:
        mediaDeeplinkData.append(result.get())

    for index, media in enumerate(mediaData):
        if mediaDeeplinkData[index]["mediaType"] == 0:
            retObj.append(Movie(
                    title=media[0],
                    originalTitle=mediaDeeplinkData[index]["originalTitle"],
                    shortDescription=media[1],
                    description=mediaDeeplinkData[index]["description"],
                    poster=media[2],
                    provider=SITE_NAME,
                    streams=mediaDeeplinkData[index]["streams"],
                ))

    return retObj
