import sys
import time
import uuid

import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from sqlalchemy import Column, MetaData, Table, create_engine, types, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# https://realpython.com/python-web-scraping-practical-introduction/
# pip install requests BeautifulSoup4
# pip install Scrapy
# pip install sqlalchemy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class CrawlCategory(scrapy.Spider):
    """
    This crawler takes a category for example,
    (https://www.bestwaywholesale.co.uk/soft-drinks) and saves the various
    information required
    """
    pass


def createEmptyDatabase():
    """
    this function will create the database, build the tables,
    setup columns and foreign keys using SQLAlchemy ORM
    """

    # create the sqlite database
    engine = create_engine('sqlite:///dataset.db', echo=True)
    Base = declarative_base()

    # each class is a table
    class Category(Base):
        __tablename__ = 'category'

        id = Column(types.Integer, primary_key=True)
        category = Column(types.String())

        children = relationship('Page')

        def __repr__(self):
            return 'id: {}, category: {}'.format(self.id, self.category)

    class Page(Base):
        __tablename__ = 'page'

        id = Column(types.Integer, primary_key=True)
        url = Column(types.String())
        HTMLContent = Column(types.String())
        dateTimeCrawled = Column(types.DateTime())
        categoryId = Column(types.Integer, ForeignKey('category.id'))

        children = relationship('Item')

        def __repr__(self):
            return '{} --> id: {}, url: {}'.format(Page.__tablename__, self.id, self.url)

    class Item(Base):
        __tablename__ = 'item'

        id = Column(types.Integer, primary_key=True)
        url = Column(types.String())
        HTMLContent = Column(types.String())
        dateTimeCrawled = Column(types.DateTime())
        pageId = Column(types.Integer, ForeignKey('page.id'))

        children = relationship(
            'ItemData', uselist=False, back_populates="item")

        def __repr__(self):
            return '{} --> id: {}, url: {}'.format(Item.__tablename__, self.id, self.url)

    class ItemData(Base):
        __tablename__ = 'itemData'

        id = Column(types.Integer, primary_key=True)
        url = Column(types.String())
        HTMLContent = Column(types.String())
        dateTimeCrawled = Column(types.DateTime())
        price = Column(types.REAL(precision=2))
        brand = Column(types.String())
        itemId = Column(types.Integer(), ForeignKey('item.id'))

        parent = relationship('Item', back_populates='itemData')

        # create the tables from the definition
        Base.metadata.create_all(engine)


if __name__ == "__main__":

    process = CrawlerProcess(
        settings={
            'FEED_FORMAT': 'json',
            'FEED_URI': 'items.json',
        }
    )
    process.crawl(QuotesSpider)
    process.start()  # the script will wait here until the crawling is complete
