# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class HotelItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    _id = Field()
    title = Field()
    rank = Field()
    rating = Field()
    total_reviews = Field()
