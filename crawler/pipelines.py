# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from statistics import mode
import statistics 
import json

class CricketcrawlerPipeline:
    def open_spider(self, spider):
        self.items = {}
        self.name = None

    def close_spider(self, spider):
        
        for item in self.items:
            assert len(self.items[item]["role"]) ==5,f'{item}'
            self.items[item]["role"] = mode(self.items[item]["role"])
        with open(self.name, 'w') as fp:
            json.dump(self.items, fp)

    def process_item(self, item, spider):
        self.name = f'fantasy_cricket/data/{item["file"]}.json'
        if item["name"] not in self.items:
            self.items[item["name"]] = {
                "role": [],
                "team": item["team"],
                "scores":{}
            }
        self.items[item["name"]]["role"].append(item["role"])
        self.items[item["name"]]["scores"][item["date"]] = item["score"]
