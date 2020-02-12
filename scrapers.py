import re
from datetime import datetime

from scrapy import Spider
from scrapy.http import TextResponse

from table_definitions.base import Session
from table_definitions.category import Category
from table_definitions.page import Page
from table_definitions.product import Product
from table_definitions.productdata import ProductData

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
    dbSession = None

    def parse(self, response: TextResponse):
        # getting data for productdata object
        r_url = response.url
        r_page = response.text
        r_time = datetime.now()

        print("scraping: {}".format(r_url))
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

        # since product and productdata has a 1 to 1 relationship, the url of product and productdata is the same
        # iterate thorugh the product table, find the matching url and create the productdata sqlalchemy object with the product object
        Product_table = crawlProduct.dbSession.query(Product).all()
        for i in Product_table:
            if i.url == r_url:
                product_data_object = ProductData(
                    url=r_url,
                    html=r_page,
                    date=r_time,
                    price=r_price,
                    brand=r_brand,
                    itemName=r_itemname,
                    size=r_size,
                    product=i
                )
                crawlProduct.dbSession.add(product_data_object)
                crawlProduct.dbSession.commit()
