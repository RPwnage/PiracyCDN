class Movie:
    def __init__(
        self,
        title: str,
        originalTitle: str = None,
        shortDescription: str = None,
        description: str = None,
        poster: str = None,
        provider: str = None,
    ):
        self.title = title
        self.originalTitle = originalTitle if originalTitle != None else None
        self.shortDescription = shortDescription if shortDescription != None else None
        self.description = description if description != None else None
        self.poster = poster if poster != None else None
        self.provider = provider if provider != None else None
