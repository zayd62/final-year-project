from table_definitions.base import Base, Session, engine
from table_definitions.author_questions import AuthorQuestions
from table_definitions.alternative_questions import AlternativeQuestions

# # test for auhthor and alt questions

# Base.metadata.create_all(engine)
# session = Session()

# auth = AuthorQuestions("english Query 1", "sql query 1")
# alt = AlternativeQuestions("obb", "jsgh", auth)
# kgdhs = AlternativeQuestions("67", "jsg#';h", auth)

# session.add(auth)
# session.add(alt)
# session.add(kgdhs)
# session.commit()
# session.close

from table_definitions.category import Category
from table_definitions.page import Page
from table_definitions.product import Product
from table_definitions.productdata import ProductData
from table_definitions.data import Data
Base.metadata.create_all(engine)
session = Session()

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

        
