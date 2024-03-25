from src.PiracyCDN import PiracyCDN

piracy = PiracyCDN()
movie = piracy.searchTitle("Star Wars")
print(movie)
