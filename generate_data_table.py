from table_definitions.base import Base, Session, engine
from table_definitions.category import Category
from table_definitions.data import Data
from table_definitions.page import Page
from table_definitions.product import Product
from table_definitions.productdata import ProductData

Base.metadata.create_all(engine)
session = Session()

def create_data_table(session):
    category_table = session.query(Category)
    # correct_products = session.query(Product).filter(Product.page).filter(Page.category_id == cat.id)
    for cat in category_table:
        correct_products = session.query(Product).filter(Product.page).filter(Page.category_id == cat.id)
        for prdct in correct_products:
            try:
                prdct_data = prdct.productData
                print(prdct_data.id)
                dta = Data(cat.category,prdct_data.price,prdct_data.brand,prdct_data.itemName,prdct_data.size)
                session.add(dta)
            except Exception:
                pass
        session.commit() 
        