# -*- coding: utf-8 -*-
from price_monitor import settings
from price_monitor.utils import reversed_timestamp, get_product_names
from datetime import datetime
import json

class CollectionStoragePipeline(object):

    def open_spider(self, spider):
        self.filename = "data/" + datetime.now().strftime("%Y%m%d") + ".json"
        self.data_stores = {}
        try:
            with open(self.filename, 'r') as fp:
                self.data_stores = json.load(fp)
        except:
            pass
            
        for product_name in get_product_names():
            if product_name not in self.data_stores:
                self.data_stores[product_name] = {}

    def process_item(self, item, spider):
        key = "{}-{}-{}".format(
            reversed_timestamp(), item.get('product_name'), item.get('retailer')
        )
        self.data_stores[item['product_name']].update({key : item})
        return item
        
    def close_spider(self, spider):
        with open(self.filename, 'w') as fp:
            json.dump(self.data_stores, fp)
