# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/

from table_definitions.base import Base, Session, engine


def create_empty_database():
    print("create empty database")
    Base.metadata.create_all(engine)
    session = Session()

    session.commit()
    session.close()
    print("created empty database successfully")


if __name__ == "__main__":
    create_empty_database()
