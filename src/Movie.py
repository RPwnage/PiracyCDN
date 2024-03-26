class Movie:
    def __init__(
        self,
        title: str,
        genre: str = None,
        originalTitle: str = None,
        shortDescription: str = None,
        description: str = None,
        poster: str = None,
        provider: str = None,
        streams: list = None,
    ):
        self.title = title
        self.genre = genre if genre != None else None
        self.originalTitle = originalTitle if originalTitle != None else None
        self.shortDescription = shortDescription if shortDescription != None else None
        self.description = description if description != None else None
        self.poster = poster if poster != None else None
        self.provider = provider if provider != None else None
        self.streams = streams if streams != None else None
