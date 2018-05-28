from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy.schema as schema
import sqlalchemy.types as types

Base = declarative_base()


class NewsItem(Base):
    __tablename__ = 'news_items'

    id = Column(types.Integer(), primary_key=True)
    title = Column(types.String(), nullable=False)
    link = Column(types.String(), nullable=False)
    published = Column(types.DateTime(), nullable=False)

    __table_args__ = (
        # Washington Post does not have pubDate
        schema.UniqueConstraint('title', 'link'), )


engine = create_engine('sqlite:///news.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all(engine)
