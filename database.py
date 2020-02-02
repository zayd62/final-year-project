# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/

from table_definitions import category
from table_definitions import page
from table_definitions import product
from table_definitions import productdata
from table_definitions.base import Base, Session, engine

Base.metadata.create_all(engine)
session = Session()

session.commit()
session.close() 