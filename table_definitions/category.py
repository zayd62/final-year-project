from sqlalchemy import Column, String, Integer
from .base import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category = Column(String)

    def __repr__(self):
        return "id: {}, category: {}".format(self.id, self.category)

    def __init__(self, category):
        self.category = category
