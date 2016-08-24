# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScholarItem(scrapy.Item):
    name        = scrapy.Field()
    email       = scrapy.Field()
    title       = scrapy.Field()
    org         = scrapy.Field()
    org_detail  = scrapy.Field()
    study_field = scrapy.Field()
    biography   = scrapy.Field()
    papers      = scrapy.Field()
    img_url     = scrapy.Field()

class FriendShip(scrapy.Item):
    first_user  = scrapy.Field()
    second_user = scrapy.Field()
