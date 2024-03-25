import requests
import json, re, os
from pathlib import Path
from .modules import *

modules = [megakino, cinemathek]


class PiracyCDN:
    def __getModuleIdentifiers(self) -> dict:
        retObj = []
        for module in modules:
            retObj.append(module.SITE_IDENTIFIER)
        return retObj

    def __getModuleNames(self) -> dict:
        retObj = []
        for module in modules:
            retObj.append(module.SITE_NAME)
        return retObj

    def __init__(self):
        self.version = "0.0.1"
        self.moduleIdentifiers = self.__getModuleIdentifiers()
        self.moduleName = self.__getModuleNames()
        self.modules = modules

    def searchTitle(title: str) -> list:
        retObj = []
        for module in self.modules:
            retObj.append(module.search(title))
        return retObj
