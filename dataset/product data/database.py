from sqlalchemy import Column, create_engine, types, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
DB_PATH = 'sqlite:///dataset.sqlite3'


def createEmptyDatabase():
    """
    this function will create the database, build the tables,
    setup columns and foreign keys using SQLAlchemy ORM
    """

    # create the sqlite database
    engine = create_engine('sqlite:///dataset.sqlite3', echo=True)
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
        item = Column(types.String())
        itemId = Column(types.Integer(), ForeignKey('item.id'))

        parent = relationship('Item', back_populates='itemData')

        def __repr__(self):
            return '{} --> id: {}, item: {}, brand: {}, price: {}'.format(ItemData.__tablename__, self.id, self, Item, self.brand, self.price)

    return Base, engine


def loadSession():
    engine = create_engine(DB_PATH)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


if __name__ == "__main__":
    Base, engine = createEmptyDatabase()
    # create the tables from the definition
    Base.metadata.create_all(engine)
