# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    seller = scrapy.Field()
    category = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    engine_code = scrapy.Field()
    version = scrapy.Field()
    production_year = scrapy.Field()
    mileage = scrapy.Field()
    engine_volume = scrapy.Field()
    fuel = scrapy.Field()
    horse_power = scrapy.Field()
    transimission = scrapy.Field()
    wd_type = scrapy.Field()
    car_type = scrapy.Field()
    seats_number = scrapy.Field()
    doors_number = scrapy.Field()
    colour = scrapy.Field()
    condition = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    
    
