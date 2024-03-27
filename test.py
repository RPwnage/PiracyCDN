from src.PiracyCDN import PiracyCDN
import logging

logging.basicConfig(level=logging.INFO)
piracy = PiracyCDN()
movie = piracy.searchTitle("The Mandalorian")
for indexSeason, season in enumerate(movie[-1].seasons):
    for indexEpisode, episode in enumerate(season):
        print(
            f"Season {str(indexSeason + 1)}\t\tEpisode {str(indexEpisode + 1)}\t\ttitle {episode.title}"
        )
