class Episode:
    def __init__(
        self,
        title: str,
        description: str = None,
        provider: str = None,
        streams: list = None,
    ):
        self.title = title
        self.description = description if description is not None else None
        self.provider = provider if provider is not None else None
        self.streams = streams if streams is not None else list()
