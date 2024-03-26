import requests, re, json, base64, m3u8

HOSTER_IDENTIFIER = "gxplayer.xyz"
HOSTER_NAME = "GXPlayer"


def extractStream(url: str):
    session = requests.Session()
    streamReq = session.get(url)
    secret = (
        (
            re.search(
                '"' + str(url.split("/watch?v=")[1]) + '"(.*).jpg', streamReq.text
            ).group(1)
        )
        .split('","')[2]
        .replace("\\", "")
        .replace("/poster", "/master.txt")
    )
    secretM3U8ContentsRaw = session.get(secret).text
    secretM3U8Object = m3u8.loads(secretM3U8ContentsRaw)
    print(re.search("(?P<url>https?://[^\s]+)", secretM3U8ContentsRaw).group("url"))
    input()
