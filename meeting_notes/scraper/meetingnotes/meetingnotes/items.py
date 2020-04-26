# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeetingNotesItem(scrapy.Item):
    # define the fields for your item here like:
    ward = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    # file_url = scrapy.Field()

    # Assigned in pipeline
    file_dl_path = scrapy.Field()
    pass
