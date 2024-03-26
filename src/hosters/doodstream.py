import requests, re, cloudscraper, math, random, time, brotli, random, gzip, logging
from bs4 import BeautifulSoup

HOSTER_IDENTIFIER = "dood.re"
HOSTER_NAME = "Dood.re"


def __makePlay(token):
    a = ""
    t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for o in range(10):
        a += t[int(math.floor(random.random() * len(t)))]
    return str(a + "?token=" + token + "&expiry=" + str(int(time.time())))


def extractStream(url: str):
    logging.info(f"[{HOSTER_NAME}]\tExtracting stream from {url}")
    scraper = cloudscraper.create_scraper()
    streamReq = scraper.get(url)
    soup = BeautifulSoup(streamReq.text, "html.parser")

    try:
        extractedToken = re.search("cookieIndex='(.*)';function", streamReq.text).group(
            1
        )
    except AttributeError:
        logging.info(f"[{HOSTER_NAME}]\tFailed to extract token from {url}")
        return None
    # Todo: replace with regex
    exctractedPassedMD5 = streamReq.text[
        (streamReq.text).find("'/pass_md5/")
        + len("'/pass_md5/") : (streamReq.text).rfind(
            "', function(data) { dpload(data);"
        )
    ]

    ss = requests.get(
        str("https://dood.re/pass_md5/" + exctractedPassedMD5),
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "br",
            "X-Requested-With": "XMLHttpRequest",
            "Dnt": "1",
            "Referer": str(url),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Te": "trailers",
        },
    )
    if (
        requests.head(
            ss.text + __makePlay(extractedToken),
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
                "Accept-Language": "en-US,en;q=0.5",
                "Range": "bytes=0-",
                "Referer": "https://dood.re/",
                "Sec-Fetch-Dest": "video",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "cross-site",
                "Accept-Encoding": "identity",
            },
        ).headers
    ) == 200 or 206:
        logging.info(f"[{HOSTER_NAME}]\tSuccessfully extracted stream from {url}")
        return str(ss.text + __makePlay(extractedToken))
