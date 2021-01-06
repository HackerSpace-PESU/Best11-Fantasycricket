# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

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
# useful for handling different item types with a single interface
import json
from statistics import mode
from itemadapter import ItemAdapter


class CricketcrawlerPipeline:
    """
    Processes output given by the crawler and stores it in a json file
    """
    def open_spider(self, spider):
        """
        Works when spider starts crawling
        """
        self.items = {}
        self.name = None

    def close_spider(self, spider):
        """
        Works when the spider stops crawling
        """
        for item in self.items:
            assert len(self.items[item]["role"]) == 5, f"{item}"
            self.items[item]["role"] = mode(self.items[item]["role"])
        with open(self.name, "w") as f_p:
            json.dump(self.items, f_p, indent=6)

    def process_item(self, item, spider):
        """
        Processes files as the items are yielded
        """
        self.name = f'app/fantasy_cricket/data/{item["file"]}.json'
        if item["name"] not in self.items:
            self.items[item["name"]] = {"role": [], "team": item["team"], "scores": {}}
        self.items[item["name"]]["role"].append(item["role"])
        self.items[item["name"]]["scores"][item["date"]] = item["score"]
