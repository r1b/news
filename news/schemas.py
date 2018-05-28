from datetime import datetime
import html
import logging
import time
from marshmallow import Schema, fields, pre_load

logger = logging.getLogger(__name__)


class SourceSchema(Schema):
    name = fields.String(required=True)
    url = fields.String(required=True)


class ConfigSchema(Schema):
    fetch_interval = fields.Integer(required=True)
    sources = fields.List(fields.Nested(SourceSchema), required=True)


class ItemSchema(Schema):
    title = fields.String(required=True)
    link = fields.String(required=True)
    published = fields.DateTime(
        data_key='published_parsed', required=True, format='rfc')

    @pre_load
    def prepare_item(self, in_data):
        # Strip html entities from title
        in_data['title'] = html.unescape(in_data['title'])

        # TODO remove query string from links

        # Convert parsed feedparser time, add if dne
        # This is kind of silly since we already have it parsed
        # FIXME use iso8601
        try:
            tt = in_data['published_parsed']
        except KeyError:
            tt = datetime.utcnow().timetuple()
        in_data['published_parsed'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', tt)
        return in_data
