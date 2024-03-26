from src.PiracyCDN import PiracyCDN
import logging

logging.basicConfig(level=logging.INFO)
piracy = PiracyCDN()
movie = piracy.searchTitle("Star Wars")
print(movie)
