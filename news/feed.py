import logging
import feedparser
from news.schemas import ItemSchema

logger = logging.getLogger(__name__)
schema = ItemSchema()


def fetch(source, queue):
    logger.info("Fetching %s for %s", source['url'], source['name'])
    rss = feedparser.parse(source['url'])

    for entry in rss.entries:
        item = schema.load(entry)
        queue.put(item.data)
