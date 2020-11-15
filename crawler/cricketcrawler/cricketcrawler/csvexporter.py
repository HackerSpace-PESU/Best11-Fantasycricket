from scrapy.exporters import CsvItemExporter


class CsvItemExporter_M(CsvItemExporter):
    """
    Fixes Bug in Scrapy
    """

    def finish_exporting(self):
        self.stream.close()
