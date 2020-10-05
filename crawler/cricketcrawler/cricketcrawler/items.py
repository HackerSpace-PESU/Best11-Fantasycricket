# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZipItem(scrapy.Item):
    # define the fields for your item here like:
    folder="zip"
    name=scrapy.Field()
    matchid = scrapy.Field()
    date = scrapy.Field()

class PlayerItem(scrapy.Item):
    folder="playernames"
    longname=scrapy.Field()
    name=scrapy.Field()
    gametype=scrapy.Field()
    retired=scrapy.Field()