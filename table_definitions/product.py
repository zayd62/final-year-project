from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    HTMLContent = Column(String)
    dateTimeCrawled = Column(Date)

    page_id = Column(Integer, ForeignKey("page.id", ondelete="CASCADE"), nullable=True)
    page = relationship("Page", cascade="delete", backref="product")

    def __repr__(self):
        return "{} --> id: {}, url: {}".format(Product.__tablename__, self.id, self.url)

    def __init__(self, url, html, date, page):
        self.url = url
        self.HTMLContent = html
        self.dateTimeCrawled = date
        self.page = page
