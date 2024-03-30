from src.PiracyCDN import PiracyCDN
import logging

logging.basicConfig(level=logging.INFO)
piracy = PiracyCDN()
movie = piracy.searchTitle("The Mandalorian")
for index, season in enumerate(movie[-1].seasons):
    print(f"Season {index + 1}:")
    for index, episode in enumerate(season):
        print(f"\tEpisode {index + 1}: {episode.title}\t{episode.streams}")
