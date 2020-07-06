"""
# File        : webscrape.py
# Author      : Jon Evans
# Last Updated: July 6, 2020
# https       : //github.com/SoundsLikeJonny
#
# This document is a part of the j_pyutils module.
#
# WebScrape encapsulates the popular functions of requests, re and time into a single class to simplify web scraping
"""

import re
import requests
import time

DEFAULT_HEADERS = {
  'cache-control'                    : 'max-age=0',                                                                                                                    \
  'rtt'                              : '50',                                                                                                                           \
  'downlink'                         : '10',                                                                                                                           \
  'ect'                              : '4g',                                                                                                                           \
  'dnt'                              : '1',                                                                                                                            \
  'upgrade-insecure-requests'        : '1',                                                                                                                            \
  'user-agent'                       : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',    \
  'accept'                           : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', \
  'service-worker-navigation-preload': 'true',                                                                                                                         \
  'sec-fetch-site'                   : 'none',                                                                                                                         \
  'sec-fetch-mode'                   : 'navigate',                                                                                                                     \
  'sec-fetch-user'                   : '?1',                                                                                                                           \
  'sec-fetch-dest'                   : 'document',                                                                                                                     \
  'accept-language'                  : 'en-US,en-PH;q=0.9,en-IN;q=0.8,en-GB;q=0.7,en;q=0.6' \
  }

class WebScrape(): 
    """
    This class allows for http get requests, regex searches and execution pausing to all happen from the same place

    The object can be initialized using the keywords below or via the dot operator

    **kwargs: 
    ======== =  = 
    url          : str           the url to search
    headers      : str           headers used in the get request
    regex_pattern: str or r''    regex pattern as a string. Converts to a raw string literal if not passed
    """

    def __init__(self, **kwargs): 
        self.url           = kwargs.get('url')
        self.headers       = kwargs.get('headers', DEFAULT_HEADERS)
        self.page          = None
        self.regex_pattern = kwargs.get('regex_pattern', '')
        self.regex_pattern = self.compile(fr'{self.regex_pattern}')
        self.found         = self.findall()
        

    def __repr__(self): 
        return repr(self.__dict__)

    
    def get(self, url: str, **kwargs) -> requests.Response: 
        """
        Calls requests.get with given arguments
        """
        if self.url != None:
            return requests.get(url, **kwargs)
        else: 
            print('Error getting URL')
            return None


    def post(self, url: str, **kwargs) -> requests.Response: 
        """ 
        Calls requests.post with given arguments
        """
        return requests.post(url,**kwargs)


    def compile(self, pattern: r'', **kwargs) -> re._compile: 
        """
        Calls re.compile passing the pattern and any other kwargs
        """
        return re.compile(pattern, **kwargs)
        

    def findall(self) -> list: 
        """
        Calls re.findall passing the pattern and text from a webpage
        """
        self.page = self.get(self.url, headers=self.headers)

        if self.page is not None: 
            self.page = self.page.text

        if self.regex_pattern != None and self.page != None:
            return re.findall(self.regex_pattern, self.page)
        else: 
            print('Error finding regex patterns')
            return None


    def sleep(self, timeout: int) -> None: 
        """
        Calls time.sleep passing the desired time to sleep
        """
        time.sleep(timeout)