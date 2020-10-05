# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from cricketcrawler.csvexporter import CsvItemExporter_M
from scrapy.exceptions import DropItem
class CricketcrawlerPipeline:
    def open_spider(self, spider):
        self.name_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.name_to_exporter.values():
            exporter.finish_exporting()

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        item2=dict(item)
        del item2["name"]
        exporter.export_item(item2)
        return item
    def _exporter_for_item(self, item):
        name = item['name']
        if name not in self.name_to_exporter:
            f = open(f'{item.folder}/{name}.csv', 'wb')
            exporter = CsvItemExporter_M(f)
            exporter.start_exporting()
            self.name_to_exporter[name] = exporter
        return self.name_to_exporter[name]


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter['name']+adapter['matchid'] in self.ids_seen:
            self.ids_seen.add(adapter['name']+adapter['matchid'])
            return item
        else:

            raise DropItem("dropped item")

