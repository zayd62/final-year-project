from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from .base import Base


class ProductData(Base):
    __tablename__ = "productData"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    HTMLContent = Column(String)
    dateTimeCrawled = Column(DateTime)
    price = Column(Float(precision=2))
    brand = Column(String)
    itemName = Column(String)
    size = Column(String)

    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=True
    )
    product = relationship(
        "Product", cascade="delete", backref=backref("productData", uselist=False)
    )

    def __repr__(self):
        return "{} --> id: {}, item: {}, brand: {}, price: {}".format(
            ProductData.__tablename__, self.id, self.itemName, self.brand, self.price
        )

    def __init__(self, url, html, date, price, brand, itemName, size, product):
        self.url = url
        self.HTMLContent = html
        self.dateTimeCrawled = date
        self.price = price
        self.brand = brand
        self.itemName = itemName
        self.size = size
        self.product = product
