from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class AlternativeQuestions(Base):
    __tablename__ = "alternativeQuestions"

    id = Column(Integer, primary_key=True)
    personName = Column(String)
    englishQuery = Column(String)

    authorQuestion_id = Column(
        Integer, ForeignKey("authorQuestion.id", ondelete="CASCADE"), nullable=True
    )
    authorquestions = relationship("AuthorQuestions", backref="page", cascade="delete")

    def __repr__(self):
        return "{} --> id: {}, url: {}".format(Page.__tablename__, self.id, self.url)

    def __init__(self, personName, englishQuery, authorQuestions):
        self.personName = personName
        self.englishQuery = englishQuery
        self.authorquestions = authorQuestions
