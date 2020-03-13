# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    comicsurl = scrapy.Field()
    name = scrapy.Field()
    pages = scrapy.Field()
    ppage = scrapy.Field()
    imageurl = scrapy.Field()
