# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TurboItem(scrapy.Item):
    ad_id = scrapy.Field()
    url = scrapy.Field()
    region = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    color = scrapy.Field()
    engine = scrapy.Field() # hecm, at gucu, tip
    odometer_km = scrapy.Field()
    transmission = scrapy.Field()
    gear = scrapy.Field()
    is_new = scrapy.Field()
    seats_count = scrapy.Field()
    prior_owners_count = scrapy.Field()
    auto_condition = scrapy.Field()
    market = scrapy.Field()
    vin = scrapy.Field()
    description = scrapy.Field()
    updated = scrapy.Field()
    number_of_views = scrapy.Field()
    price_original = scrapy.Field()
    price_azn = scrapy.Field()
    status_order = scrapy.Field()
    damaged = scrapy.Field()
    product_extras = scrapy.Field()
    horsepower = scrapy.Field()
    fuel_type = scrapy.Field()


