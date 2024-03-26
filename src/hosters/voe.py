import requests, logging, re, json, base64

HOSTER_IDENTIFIER = "voe.sx"
HOSTER_NAME = "Voe.sx"


def extractStream(url: str) -> str:
    """
    Extracts the HLS .m3u8 file from the Voe.sx player page.

    Args:
        url (str): The URL of the Voe.sx player page.

    Returns:
        str: The m3u8 link.
    """
    logging.info(f"[{HOSTER_NAME}]\tExtracting stream from {url}")
    res = requests.get(url)
    m3u8 = re.search("'hls': '(.*)',", res.text).group(1)
    if len(m3u8) > 10 and "https://" in m3u8:
        logging.info(f"[{HOSTER_NAME}]\tSuccessfully extracted stream from {url}")
        return m3u8
    return None
