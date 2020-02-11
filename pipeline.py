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
category_url = sys.argv[1]
category_name = sys.argv[2]

# open database session and make it available to the crawler
session = Session()


def crawl_category(session, url, catName):
    """
    Given a url, the function will crawl the category and insert the crawled pages into the database. 
    it will also return the generate category object (using catName to name the category) from which you are able to determine
    the page entries created in the database due to the one-to-many relationship between the category and the page
    """
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

    # Give the crawler access to the database session
    CrawlCategory.dbSession = session

    # Give the crawler the url to scrape
    CrawlCategory.start_urls = [url]

    # create category object and add to session
    cat = Category(catName)
    session.add(cat)

    # Give the crawler the category object
    CrawlCategory.catObject = cat

    # run the crawler
    print("starting crawl for category")
    process.crawl(CrawlCategory)
    process.start()  # the script will wait here until the crawling is complete
    print("finished crawl for category. Committing the change to the database")
        
    # save the results of the crawling to the database
    session.commit()
    return cat

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


create_category_object = crawl_category()
