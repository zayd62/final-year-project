import sys

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer, reactor

from html_parse.page_product import parse
from scrapers import CrawlCategory, crawlProduct
from table_definitions.base import Session
from table_definitions.category import Category
from table_definitions.page import Page
from table_definitions.product import Product
from table_definitions.productdata import ProductData

# cli arguments
# 1: category url
# 2: category name

# crawl the category
category_url = sys.argv[1]
category_name = sys.argv[2]

# open database session and make it available to the crawler
session = Session()


def page_parse(session, category_id):
    print("Starting page --> product HTML parse")
    parse(session, category_id)
    print("HTML parse complete. scraping productdata")


def product_data_urls(session, cat_id):
    # return the products from the database with the appropriate category id
    correct_products = (
        session.query(Product)
        .filter(Product.page)
        .filter(Page.category_id == cat_id)
        .all()
    )
    urlList = []
    for i in correct_products:
        # crawlProduct.dbSession = session
        # crawlProduct.productObject = i
        urlList.append(i.url)

    return urlList
    print("completed product --> productdata conversion")


configure_logging()
runner = CrawlerRunner()
category_settings = {
    "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "DOWNLOAD_DELAY": "1",
    "AUTOTHROTTLE_ENABLED": "True",
    "HTTPCACHE_ENABLED": "False",
}

product_settings = {
    "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "DOWNLOAD_DELAY": "1",
    "AUTOTHROTTLE_ENABLED": "True",
    "HTTPCACHE_ENABLED": "False",
    "DOWNLOADER_MIDDLEWARES": {
        "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
        "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    }
}

# "ROTATING_PROXY_LIST_PATH": 'proxies/proxy.txt'

@defer.inlineCallbacks
def crawl(session, category_url, category_name):
    # create category object and commit to db
    cat = Category(category_name)
    session.add(cat)
    session.commit()

    # add session, custom settings and category object to category crawler
    CrawlCategory.dbSession = session
    CrawlCategory.start_urls = [category_url]
    CrawlCategory.catObject = cat
    CrawlCategory.custom_settings = category_settings

    print("starting crawl for category")
    yield runner.crawl(CrawlCategory)
    print("finished crawl for category. Committing the change to the database")

    page_parse(session, cat.id)
    urls = product_data_urls(session, cat.id)
    
    # add session, custom settings and starting urls object to category crawler
    crawlProduct.dbSession = session
    crawlProduct.start_urls = urls
    crawlProduct.custom_settings = product_settings
    yield runner.crawl(crawlProduct)


crawl(session, category_url, category_name)
reactor.run()  # the script will block here until the last crawl call is finished
reactor.stop()