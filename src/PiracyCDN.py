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
    """
    This class provides a unified interface for searching for media content on various piracy websites.
    It uses a plug-in system, where each plug-in implements a specific website and provides the search functionality.
    The plug-ins are stored in a list, and are accessed using their site identifiers.
    The search method takes a search query, and returns a list of results.

    Example usage:

    ```
    from PiracyCDN import PiracyCDN
    cdn = PiracyCDN()
    results = cdn.search("Spider-Man: No Way Home")
    for result in results:
        print(result)
    ```

    """

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
        """
        Searches for a media title on all the plug-in websites.

        Parameters:
            title (str): The media title to search for

        Returns:
            list: A list of search results
        """
        # Create threads to fasten up the search process
        pool = ThreadPool(processes=2)
        retObj = []
        async_result = list()
        for index, module in enumerate(self.modules):
            async_result.append(pool.apply_async(module.search, (str(title),)))

        for result in async_result:
            retObj.append(result.get())

        return list(flatten(retObj))
