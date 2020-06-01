# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimalPicturesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()  # 图片名
    title = scrapy.Field()  # 图片标题
    url = scrapy.Field()   # 图片下载路径
    status = scrapy.Field()  # 下载状态
