import logging
from sqlalchemy.exc import IntegrityError
from news.models import NewsItem, Session

logger = logging.getLogger('persist')
session = Session()


def persist(queue):
    while True:
        fetched_item = queue.get()
        news_item = NewsItem(**fetched_item)
        session.add(news_item)

        try:
            session.commit()
            logger.info('Added %s', news_item.title)
        except IntegrityError:
            session.rollback()

        queue.task_done()
