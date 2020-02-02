import sys
from datetime import datetime
from database import loadSessionBase
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse

# https://realpython.com/python-web-scraping-practical-introduction/
# pip install requests BeautifulSoup4
# pip install Scrapy
# pip install sqlalchemy


URL = None


class CrawlCategory(Spider):
    """
    This crawler takes a category for example,
    (https://www.bestwaywholesale.co.uk/soft-drinks) and saves the various
    information required
    """

    # name of spider
    name = "category"
    crawlCategoryName = None
    crawlCategoryId = None

    def parse(self, response: TextResponse):
        # getting the data required to store in the pages table
        r_url = response.url
        r_page = response.text
        r_time = datetime.utcnow()

        # loading sqlite db using sqlalchemy
        session, base = loadSessionBase()

        # creating page table
        pageobj = base.classes.page

        # creating page row
        page_objectToCommit = pageobj(
            url=r_url,
            HTMLContent=r_page,
            dateTimeCrawled=r_time,
            categoryId=CrawlCategory.crawlCategoryId,
        )
        session.add(page_objectToCommit)
        session.commit()

        # calculating the url for the next page
        next_page = response.css("li.next a").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


if __name__ == "__main__":
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
    CrawlCategory.start_urls = [sys.argv[2]]
    CrawlCategory.crawlCategoryName = sys.argv[1]

    # loading sqlite db using sqlalchemy
    session, base = loadSessionBase()

    # writing information to category table
    categoryobj = base.classes.category
    category_objectToCommit = categoryobj(category=CrawlCategory.crawlCategoryName)
    session.add(category_objectToCommit)
    session.commit()

    # getting id of newly added row to category table
    categoryId = category_objectToCommit.id

    # adding the id to spider object
    CrawlCategory.crawlCategoryId = categoryId

    process.crawl(CrawlCategory)
    process.start()  # the script will wait here until the crawling is complete
