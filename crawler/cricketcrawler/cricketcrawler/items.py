# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Baseitem(scrapy.Item):
    file = ""
    folder = scrapy.Field()
    unique = []

    def get_key(self):
        d = dict(self)
        key = self.file
        key += "".join([d[i] for i in self.unique])


class MatchidItem(Baseitem):
    file = "match_ids"
    name = scrapy.Field()
    matchid = scrapy.Field()
    date = scrapy.Field()
    unique = ["name", "matchid"]


class PlayerItem(Baseitem):
    file = "id_names"
    longname = scrapy.Field()
    name = scrapy.Field()
    gametype = scrapy.Field()
    retired = scrapy.Field()
    unique = ["name", "gametype"]


class BowlingItem(Baseitem):
    file = "bowling"
    matchid = scrapy.Field()
    overs = scrapy.Field()
    score = scrapy.Field()
    economy = scrapy.Field()
    name = scrapy.Field()
    folder= scrapy.Field()


class BattingItem(Baseitem):
    file = "batting"
    matchid = scrapy.Field()
    score = scrapy.Field()
    strike_rate = scrapy.Field()
    name = scrapy.Field()
    folder= scrapy.Field()

class wicketkeepingItem(Baseitem):
    file = "wicketkeeping"
    matchid = scrapy.Field()
    score = scrapy.Field()
    name = scrapy.Field()
    folder= scrapy.Field()