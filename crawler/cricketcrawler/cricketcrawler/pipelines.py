# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter


class CricketcrawlerPipeline:
    def open_spider(self, spider):
        self.name_to_exporter = {}
        self.seen = list()

    def close_spider(self, spider):
        for exporter, fp in self.name_to_exporter.values():
            exporter.finish_exporting()
            fp.close()

    def process_item(self, item, spider):
        exporter= self._exporter_for_item(item)
        del item["folder"]
        item2 = dict(item)
        exporter.export_item(item2)
        return item

    def _exporter_for_item(self, item):
        name = f'../../data_crawler/{item["folder"]}/{item.file}.csv'
        if name not in self.name_to_exporter:
            f = open(name, "wb")
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.name_to_exporter[name] = exporter, f
        return self.name_to_exporter[name][0]