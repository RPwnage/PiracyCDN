import logging, requests

HOSTER_IDENTIFIER = "vidmoly.to"
HOSTER_NAME = "Vidmoly.to"


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
    if res.status_code == 404:
        logging.info(
            f"[{HOSTER_NAME}]\tFailed to extract stream from {url} (link seems to be dead)"
        )
        return None

    m3u8 = res.text[
        res.text.find('[{file:"') + len('[{file:"') : res.text.rfind('"}],')
    ]

    logging.info(f"[{HOSTER_NAME}]\tSuccessfully extracted stream from {url}")

    return m3u8
