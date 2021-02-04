# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):

    name = scrapy.Field()
    image = scrapy.Field()
    role = scrapy.Field()
    player_id = scrapy.Field()


class ScoreItem(scrapy.Item):

    runs = scrapy.Field()
    boundaries = scrapy.Field()
    sixes = scrapy.Field()
    wicket = scrapy.Field()
    Maiden = scrapy.Field()
    Catch = scrapy.Field()
    Stump = scrapy.Field()
    match_id = scrapy.Field()


class LiveMatchItem(scrapy.Item):

    team1 = scrapy.Field()
    team2 = scrapy.Field()
    match_id = scrapy.Field()
    team1_squad = scrapy.Field()
    team2_squad = scrapy.Field()
    team1_id = scrapy.Field()
    team2_id = scrapy.Field()
