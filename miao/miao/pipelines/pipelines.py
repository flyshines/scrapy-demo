# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from miao.db.sql import Sql
from miao.items import MiaoItem


class MySqlPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, MiaoItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] >= 1:
                print('已经存在改值了:' + name_id)
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert_dd_name(xs_name, xs_author, category, name_id)
                print('已保存小说标题了:' + xs_name)
