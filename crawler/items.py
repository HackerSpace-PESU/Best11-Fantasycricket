# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    role = scrapy.Field()
    score = scrapy.Field()
    team = scrapy.Field()
    date = scrapy.Field()
    file = scrapy.Field()
