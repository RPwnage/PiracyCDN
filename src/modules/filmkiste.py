import requests, logging
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

from ..hosters import *

HOSTERS = []
SITE_IDENTIFIER = "filmkiste"
SITE_NAME = "Filmkiste"


def __fetchDataFromDeeplink(url: str) -> dict:
    res = requests.get(str(url))
    soup = BeautifulSoup(res.text, "html.parser")
    description = str((soup.find("div", class_="page__text")).text)


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
        retObj.append([])

    return retObj
