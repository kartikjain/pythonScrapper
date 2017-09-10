from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
import logging
import json

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['_id'])
            return item


class JsonPipeline(object):
    def __init__(self):
        self.file1 = open("items.json", 'wb')
        self.file1.truncate()
        self.file2 = open("reviews.json", 'wb')
        self.file2.truncate()
        self.exporter1 = JsonItemExporter(self.file1, encoding='utf-8', ensure_ascii=False)
        self.exporter2 = JsonItemExporter(self.file2, encoding='utf-8', ensure_ascii=False)
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()
    def close_spider(self, spider):
    	logging.info("spider force closed")
    	self.exporter1.finish_exporting()
        self.exporter2.finish_exporting()
        self.file1.close()
        self.file2.close()

    def process_item(self, item, spider):
        if 'review' in item.keys():
            self.exporter2.export_item(item)
        else:
            self.exporter1.export_item(item)
        return item