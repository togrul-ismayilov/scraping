from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.utils.response import response_status_message
from turbobot.items import TurboItem
from urllib.parse import urlencode



def get_proxy_url(self, url):
    payload = {'api_key': self.settings.get('SCRAPEOPS_API_KEY'), 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class TurbospiderSpider(scrapy.Spider):
    name = "turbospider"
    allowed_domains = ["turbo.az", "proxy.scrapeops.io"]
    start_urls = ["https://turbo.az"]


    def start_requests(self):
        yield scrapy.Request(url = self.start_urls[0], callback=self.parse)

    def parse(self, response):

        cars = response.css('a.products-i__link')
        if cars is None:
            return

        if cars:
            for car in cars:
                relative_url = car.css('::attr(href)').get()
                car_url = 'https://turbo.az/' + relative_url
                yield scrapy.Request(url=car_url, callback=self.parse_car_details)


            # Get the next page number by extracting the page number from the URL
            if '?page=' in response.url:
                current_page = int(response.url.split('=')[-1])
                next_page = current_page + 1
            else:
                # For the first page, start with page 2
                current_page = 1
                next_page = 2

            # Build the URL for the next page
            next_page_url = f'https://turbo.az/autos?page={next_page}'
            # Check if the next page has content by making a request
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_car_details(self, response):

        car_item = TurboItem()

        car_item['url'] = response.url
        car_item['region'] = response.css('label[for="ad_region"] + span.product-properties__i-value::text').get()
        car_item['make'] = response.css('label[for="ad_make_id"] + span.product-properties__i-value a::text').get()
        car_item['model'] = response.css('label[for="ad_model"] + span.product-properties__i-value a::text').get()
        car_item['year'] = response.css('label[for="ad_reg_year"] + span.product-properties__i-value a::text').get()
        car_item['category'] = response.css('label[for="ad_category"] + span.product-properties__i-value::text').get()
        car_item['color'] = response.css('label[for="ad_color"] + span.product-properties__i-value::text').get()
        car_item['engine'] = response.css('label[for="ad_engine_volume"] + span.product-properties__i-value::text').get()
        car_item['odometer_km'] = response.css('label[for="ad_mileage"] + span.product-properties__i-value::text').get()
        car_item['gear'] = response.css('label[for="ad_gear"] + span.product-properties__i-value::text').get()
        car_item['transmission'] = response.css('label[for="ad_transmission"] + span.product-properties__i-value::text').get()
        car_item['is_new'] = response.css('label[for="ad_new"] + span.product-properties__i-value::text').get()
        car_item['seats_count'] = response.css('label[for="ad_seats_count"] + span.product-properties__i-value::text').get()
        car_item['prior_owners_count'] = response.css('label[for="ad_prior_owners_count"] + span.product-properties__i-value::text').get()
        car_item['auto_condition'] = response.css('label[for="ad_Vəziyyəti"] + span.product-properties__i-value::text').get()
        car_item['market'] = response.css('label[for="ad_market"] + span.product-properties__i-value::text').get()
        car_item['description'] = "\n".join(response.css('.product-description__content p::text').getall())
        car_item['vin'] = response.css('.js-description-content p br::text').get()
        car_item['updated'] = response.css('.product-statistics__i span::text').get()
        car_item['number_of_views'] = response.css('.product-statistics__i span::text').getall()[1]
        car_item['price_original'] = response.css('.product-price__i.product-price__i--bold::text').get()
        car_item['price_azn'] = response.css('.product-price__i.tz-mt-10::text').get()
        car_item['status_order'] = response.css('.product-shop__status_order::text').get()
        car_item['damaged'] = response.css('label[for="ad_Qəzalı"] + span.product-properties__i-value::text').get()
        car_item['product_extras'] = response.css('.product-extras__i::text').getall()

        yield car_item