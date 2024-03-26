from .Episode import Episode


class Series:
    def __init__(self, title: str, poster: str = None, seasons: list = None):
        self.title = title
        self.poster = poster if poster is not None else None
        self.seasons = seasons if seasons is not None else list()

    def addEpisode(self, season: int, episode: Episode):
        self.seasons[season].append(episode)
