import requests
import json, re, os
from pathlib import Path
from .modules import *
from multiprocessing.pool import ThreadPool
from collections.abc import Iterable

modules = [megakino, cinemathek]


def flatten(list):
    for item in list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


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
        self.moduleNames = self.__getModuleNames()
        self.modules = modules

    def searchTitle(self, title: str) -> list:
        # Create threads to fasten up the search process
        pool = ThreadPool(processes=2)
        retObj = []
        async_result = list()
        for index, module in enumerate(self.modules):
            async_result.append(pool.apply_async(module.search, (str(title),)))

        for result in async_result:
            retObj.append(result.get())

        return list(flatten(retObj))
