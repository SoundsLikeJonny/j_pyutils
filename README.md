# j_pyutils

Custom tools to simplify the process of writing... well, more tools!

**TODO**

* [ ] Add BeautifulSoup functionality to webscrape.py
* [ ] Create a logtxt.py to for quick logging

## webscrape.py

Simplified object-oriented web scraping.

Example:

```
url = "amazon.ca/someproduct"
scrape_site = WebScrape(url=url, regex_pattern=r'CDN\$.(\d\d\d)')
results_list = scrape_site.found  # ['234', '367', '332', '825']



```
