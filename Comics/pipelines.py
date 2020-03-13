# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Comics import settings
import pymysql.cursors
import scrapy

class ComicsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            port = settings.MYSQL_PORT,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWD,
            charset = 'utf8',
            use_unicode=True,
        )
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        mysql_insert = ('insert into Comics(comicsurl,name,pages,ppage,imageurl) VALUES ("%s","%s","%s","%s","%s")'%
                       (item['comicsurl'], item['name'], item['pages'] ,item['ppage'],item['imageurl']))

        self.cursor.execute(mysql_insert)
        self.connect.commit()

        return item
