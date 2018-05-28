import yaml
from news.schemas import ConfigSchema

schema = ConfigSchema()
config = schema.load(yaml.load(open("news/config.yml", 'r'))).data
