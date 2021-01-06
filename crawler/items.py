# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

"""
    Copyright (C) 2020  Royston E Tauro & Sammith S Bharadwaj & Shreyas Raviprasad

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import scrapy


class PlayerItem(scrapy.Item):
    """
    Class scrapes name of the player
    Role of the player
    Score he scored in that game
    Team he is playing for
    Date of the match
    File it has been stored in
    """
    name = scrapy.Field()
    role = scrapy.Field()
    score = scrapy.Field()
    team = scrapy.Field()
    date = scrapy.Field()
    file = scrapy.Field()
