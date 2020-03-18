# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
pth = '/media/zayd/Common/University/Year 3/Final Year Project/git-repository/dataset.sqlite3'
engine = create_engine("sqlite:///" + pth)
Session = sessionmaker(bind=engine)

Base = declarative_base()
