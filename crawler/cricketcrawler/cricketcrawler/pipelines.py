# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class CricketcrawlerPipeline:
    def open_spider(self, spider):
        self.name_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.name_to_exporter.values():
            exporter.finish_exporting()

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        name = adapter['name']
        if name not in self.name_to_exporter:
            f = open('zip/{}.csv'.format(name), 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.name_to_exporter[name] = exporter
        return self.name_to_exporter[name]
