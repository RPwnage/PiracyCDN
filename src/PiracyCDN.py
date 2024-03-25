import requests
import json, re, os
from pathlib import Path


class PiracyCDN:
    def __getModules(self) -> dict:
        retObj = []
        for file in os.listdir(str(Path(__file__).parent.absolute()) + "/modules"):
            if file.endswith(".module.py") and file != "example.module.py":
                retObj.append(file)
        return retObj

    def __init__(self):
        self.version = "0.0.1"
        self.modules = self.__getModules()

    def searchTitle(title: str) -> list:
        pass

    def getTitleInfo(movieId: int) -> dict:
        pass

    def getVideoInfo(movieId: int) -> dict:
        pass

    def getAudioInfo(movieId: int) -> dict:
        pass
