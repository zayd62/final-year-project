import os
import sys

from bs4 import BeautifulSoup as bs
from sqlalchemy.orm import Session as ses

if __name__ == "__main__":
    sys.path.append("/media/zayd/Common/University/Year 3/Final Year Project/code")
    from table_definitions.base import Session
    from table_definitions.category import Category
    from table_definitions.page import Page
    from table_definitions.product import Product

# connect to database
session: ses
session = Session()

# get all the elements in the page table
page_table = session.query(Page).all()

# iterate through all the rows in the page table (i is a row in the page table)
for i in page_table:
    print("the url is {}".format(i.url))
    # select the raw html
    soup = bs(i.HTMLContent, "html.parser")

    # select the table containing all the Products
    all_products = soup.find("ul", class_="shop-products gridview")

    # find each product. each product is represented as an <li> element
    all_products_lst = all_products.find_all("li")

    # iterate through (html) list of products ignoring the hidden columns
    for j in all_products_lst:
        try:
            hidden = j["class"]
        except KeyError as e:
            # not a hidden product. i.e. it is an actual product
            bestway_base_url = "https://www.bestwaywholesale.co.uk"

            # collect necessary db info
            calculated_url = bestway_base_url + j["data-ga-product-url"]
            html = str(j)


            # create product object to be commited to the db
            product_obj = Product(url=calculated_url, html=html, page=i)
            session.add(product_obj)

session.commit()
session.close()
# soup = bs(page_table[0].HTMLContent, "html.parser")
# all_products = soup.find("ul", class_="shop-products gridview")
# all_products_lst = all_products.find_all("li")
# all_products_lst["class"]
# all_products_lst["data-ga-product-url"]
