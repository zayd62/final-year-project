from table_definitions.base import Base, Session, engine
from table_definitions.data_split import DataSplit

session = Session()
q = session.query(DataSplit)
columns = DataSplit.__table__.columns.keys()
for f in q:
    for key in columns:
        value = f.__getattribute__(key)
        if type(value) is str:
            value = value.lower()
            f.__setattr__(key, value)
        session.add(f)
session.commit()

