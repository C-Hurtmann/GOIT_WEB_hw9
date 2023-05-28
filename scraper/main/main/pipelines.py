# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from pathlib import Path
import json


class MainPipeline:

    def process_item(self, item, spider):
        root = os.path.dirname(os.path.dirname(os.getcwd()))
        adapter = ItemAdapter(item)
        dict_item = adapter.asdict()

        if dict_item.get('born_date'):
            storage = Path(root + '/database/jsons/authors.json')
        elif dict_item.get('tags'):
            storage = Path(root + '/database/jsons/quotes.json')

        with open(storage, 'a') as f:
            json.dump(dict_item, f, indent=4)
            f.write('\r')
        return item
