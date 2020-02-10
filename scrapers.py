import re
import sys
from datetime import datetime

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse

from table_definitions.base import Session
from table_definitions.category import Category
from table_definitions.page import Page

# https://realpython.com/python-web-scraping-practical-introduction/
# pip install requests BeautifulSoup4
# pip install Scrapy
# pip install sqlalchemy


class CrawlCategory(Spider):
    """
    This crawler takes a category for example,
    (https://www.bestwaywholesale.co.uk/soft-drinks) and saves the various
    information required
    """

    name = "category"

    # SQLAlchemy category object
    catObject = None

    # SQLAlchemy session object
    dbSession = None

    def parse(self, response: TextResponse):
        # getting the data required to store in the pages table
        r_url = response.url
        r_page = response.text
        r_time = datetime.now()
        print("scraping: {}".format(r_url))
        # create SQLAlchemy page object
        pge = Page(
            url=r_url, html=r_page, date=r_time, category=CrawlCategory.catObject
        )

        # add page object
        CrawlCategory.dbSession.add(pge)

        # calculating the url for the next page
        next_page = response.css("li.next a").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class crawlProduct(Spider):
    """
    This crawler scrapes individual product pages and extracts appropriate information
    """

    name = "product"

    def parse(self, response: TextResponse):
        # getting data for productdata object
        r_url = response.url
        r_page = response.text
        r_time = datetime.now()

        # get price
        r_price = response.css(".prodtable tr:nth-of-type(2) td::text").get()
        r_price = "".join(
            re.findall(r"([\d,.])", r_price)
        )  # use regex to remove the currency symbol

        # get brand
        r_brand = response.css(".prodtable tr:nth-of-type(8) td::text").get()

        # get item name
        r_itemname = response.css(".productpagedetail-inner .prodname::text").get()

        # get item size
        r_size = response.css(".prodtable tr:nth-of-type(4) td::text").get()
        r_size = "".join(re.findall(r"([\d,.])", r_size))

        yield {
            "url": r_url,
            "HTMLContent": r_page,
            "dateTimeCrawled": r_time,
            "price": r_price,
            "brand": r_brand,
            "itemName": r_itemname,
            "size": r_size,
        }


def crawl_wrapper_category(session):
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

    CrawlCategory.dbSession = session

    # url to scrape
    url = sys.argv[1]
    CrawlCategory.start_urls = [url]

    # create category object and add to session
    catName = sys.argv[2]
    cat = Category(catName)
    session.add(cat)

    # make category object available to the crawler
    CrawlCategory.catObject = cat

    # run the crawler
    print("starting crawl")
    process.crawl(CrawlCategory)
    process.start()  # the script will wait here until the crawling is complete
    print("crawl finished")


def crawl_wrapper_productdata():
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
    crawlProduct.start_urls = [
        "https://www.bestwaywholesale.co.uk/product/586208-1",
        "https://www.bestwaywholesale.co.uk/product/412060-1",
    ]
    process.crawl(crawlProduct)
    process.start()


if __name__ == "__main__":

    # open database session and make it available to the crawler
    session = Session()

    # # invoke crawler for category
    # crawl_wrapper_category(session)

    # invoke crawler for productdata
    crawl_wrapper_productdata()

    # commit and close the database session
    session.commit()
    session.close()
