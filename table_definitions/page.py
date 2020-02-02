from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    HTMLContent = Column(String)
    dateTimeCrawled = Column(Date)

    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    category = relationship("Category", backref="page")

    def __repr__(self):
        return "{} --> id: {}, url: {}".format(Page.__tablename__, self.id, self.url)

    def __init__(self, url, html, date, category):
        self.url = url
        self.HTMLContent = html
        self.dateTimeCrawled = date
        self.category = category
