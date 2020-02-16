import re
from datetime import datetime

from scrapy import Spider
from scrapy.http import TextResponse

from html_parse.productdata import parse as product_data_html_parse
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
        print(__file__, "CrawCategory.parse()", "scraping for pages: {}".format(r_url))
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

        print("scraping for productData: {}".format(r_url))

        dct = product_data_html_parse(response.css(".prodtable").get())
        remove = False
        try:
            # get price
            r_price = dct["RSP"]
            r_price = "".join(
                re.findall(r"([\d,.])", r_price)
            )  # use regex to remove the currency symbol

            # get brand
            r_brand = dct['Brand']

            # get item name
            r_itemname = response.css(".productpagedetail-inner .prodname::text").get()

            # get item size
            r_size = dct['Pack Size']
            r_size = "".join(re.findall(r"([\d,.])", r_size))
        except KeyError as e:
            print(e)
            print("Missing data, remove ")
            remove = True

        # since product and productdata has a 1 to 1 relationship, the url of product and productdata is the same
        # iterate thorugh the product table, find the matching url and create the productdata sqlalchemy object with the product object
        Product_table = crawlProduct.dbSession.query(Product).all()
        for i in Product_table:
            # if there is a matcging url, we found the matching product
            if i.url == r_url:
                # check if any of the scraped data has none values. if true, delete the product entry
                if remove:
                    crawlProduct.dbSession.query(Product).filter(
                        Product.id == i.id
                    ).delete()
                else:
                    product_data_object = ProductData(
                        url=r_url,
                        html=r_page,
                        date=r_time,
                        price=r_price,
                        brand=r_brand,
                        itemName=r_itemname,
                        size=r_size,
                        product=i,
                    )
                    crawlProduct.dbSession.add(product_data_object)
                crawlProduct.dbSession.commit()
