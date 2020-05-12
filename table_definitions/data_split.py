from sqlalchemy import Column, String, Integer, Float
from .base import Base


class DataSplit(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    price = Column(Float(precision=2))
    brand = Column(String)
    itemname = Column(String)
    size = Column(String)
    unit = Column(String)

    def __repr__(self):
        return "id: {}, itemname: {}, size: {}".format(self.id, self.itemName, self.size)

    def __init__(self, category, price, brand, itemname, size):
        self.category = category
        self.price = price
        self.brand = brand
        self.itemName = itemname
        self.size = size

