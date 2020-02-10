import sys

from scrapy.crawler import CrawlerProcess

from html_parse.page_product import parse
from scrapers import CrawlCategory, crawlProduct
from table_definitions.base import Session

# CONSTANTS
PRODUCT_SAVE = "items.csv"
# cli arguments
# 1: category url
# 2: category name

# crawl the category
category_url = None

# create crawler process for category crawling 
process = CrawlerProcess(
    settings={
        "FEED_FORMAT": "json",
        "FEED_URI": "items.json",
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "DOWNLOAD_DELAY": "1",
        "AUTOTHROTTLE_ENABLED": "True",
        "HTTPCACHE_ENABLED": "False",
    }
)

# open database session and make it available to the crawler
session = Session()
# CrawlCategory.dbSession = session

# # url to scrape
# url = sys.argv[1]
# CrawlCategory.start_urls = [url]

# # create category object and add to session
# catName = sys.argv[2]
# cat = Category(catName)
# session.add(cat)

# # make category object available to the crawler
# CrawlCategory.catObject = cat

# # run the crawler
# print("starting crawl for category")
# process.crawl(CrawlCategory)
# process.start()  # the script will wait here until the crawling is complete
# print("finished crawl for category. Committing the change to the database")
# session.commit()

print("Starting page --> product HTML parse")
parse(session)
print("HTML parse complete. scraping productdata")

# create crawling process for productdata crawling
process = CrawlerProcess(
    settings={
        "FEED_FORMAT": "csv",
        "FEED_URI": "items.csv",
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "DOWNLOAD_DELAY": "1",
        "AUTOTHROTTLE_ENABLED": "True",
        "HTTPCACHE_ENABLED": "False",
    }
)
