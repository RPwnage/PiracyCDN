import requests
import json, re, os
from pathlib import Path
from .modules import *
from multiprocessing.pool import ThreadPool
from collections.abc import Iterable

modules = [megakino, cinemathek, filmkiste]


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
        self.providers = self.__getModuleIdentifiers()
        self.modules = modules

    def searchTitle(self, title: str, provider: str = None) -> list:
        """
        Searches for a media title on all the plug-in websites.

        Parameters:
            title (str): The media title to search for
            provider (str): The site identifier of the website to use for the search

        Returns:
            list: A list of search results
        """
        # Create threads to fasten up the search process
        title = title.lower()
        pool = ThreadPool(processes=2)
        retObj = []
        async_result = list()
        for index, module in enumerate(self.modules):
            if provider != None and module.SITE_IDENTIFIER == provider:
                async_result.append(pool.apply_async(module.search, (str(title),)))
            elif provider == None:
                async_result.append(pool.apply_async(module.search, (str(title),)))

        for result in async_result:
            retObj.append(result.get())

        return list(flatten(retObj))
