from sqlalchemy import Column, ForeignKey, MetaData, create_engine, types
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
DB_PATH = 'sqlite:///dataset.sqlite3'
BASE = declarative_base()

# each class is a table


class Category(BASE):
    __tablename__ = 'category'

    id = Column(types.Integer, primary_key=True)
    category = Column(types.String())

    children = relationship('Page')

    def __repr__(self):
        return 'id: {}, category: {}'.format(self.id, self.category)


class Page(BASE):
    __tablename__ = 'page'

    id = Column(types.Integer, primary_key=True)
    url = Column(types.String())
    HTMLContent = Column(types.String())
    dateTimeCrawled = Column(types.DateTime())
    categoryId = Column(types.Integer, ForeignKey(
        'category.id'), nullable=True)

    children = relationship('Product')

    def __repr__(self):
        return '{} --> id: {}, url: {}'.format(Page.__tablename__, self.id, self.url)


class Product(BASE):
    __tablename__ = 'product'

    id = Column(types.Integer, primary_key=True)
    url = Column(types.String())
    HTMLContent = Column(types.String())
    dateTimeCrawled = Column(types.DateTime())
    pageId = Column(types.Integer, ForeignKey('page.id'), nullable=True)

    actualProductid = relationship(
        'ActualProduct', backref="owner", uselist=False)

    def __repr__(self):
        return '{} --> id: {}, url: {}'.format(Product.__tablename__, self.id, self.url)


class ActualProduct(BASE):
    __tablename__ = 'actualProduct'

    id = Column(types.Integer, primary_key=True)
    url = Column(types.String())
    HTMLContent = Column(types.String())
    dateTimeCrawled = Column(types.DateTime())
    price = Column(types.REAL(precision=2))
    brand = Column(types.String())
    itemName = Column(types.String())

    productId = Column(types.Integer(), ForeignKey(
        'product.id'), nullable=True)

    # parent = relationship('Product', back_populates='children')

    def __repr__(self):
        return '{} --> id: {}, item: {}, brand: {}, price: {}'.format(ActualProduct.__tablename__, self.id, self.itemName, self.brand, self.price)


def createEmptyDatabase():
    """
    this function will create the database, build the tables,
    setup columns and foreign keys using SQLAlchemy ORM
    """

    # create the sqlite database
    engine = create_engine('sqlite:///dataset.sqlite3', echo=True)

    return engine


def load_engine():
    return create_engine(DB_PATH)


def loadSession():
    engine = load_engine()
    return Session(engine)


def loadBaseAuto():
    engine = load_engine()
    auto_base = automap_base()
    auto_base.prepare(engine, reflect=True)
    return auto_base


def loadSessionBase():
    return loadSession(), loadBaseAuto()


if __name__ == "__main__":
    engine = createEmptyDatabase()
    # create the tables from the definition
    BASE.metadata.create_all(engine)
