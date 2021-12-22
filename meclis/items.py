# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeclisItem(scrapy.Item):
    name = scrapy.Field()
    party = scrapy.Field()
    bill_prop_count = scrapy.Field()
    res_prop_count = scrapy.Field()
    speech_count = scrapy.Field()

    pass
