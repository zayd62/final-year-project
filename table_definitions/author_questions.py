from sqlalchemy import Column, String, Integer
from .base import Base


class AuthorQuestions(Base):
    __tablename__ = "authorQuestion"

    id = Column(Integer, primary_key=True)
    englishQuery = Column(String)
    SQLQuery = Column(String)


    def __repr__(self):
        return "id: {}, englishQuery: {}, SQLQuery: {}".format(self.id, self.englishQuery, self.SQLQuery)

    def __init__(self, englishquery, sqlquery):
        self.englishQuery = englishquery
        self.SQLQuery = sqlquery

