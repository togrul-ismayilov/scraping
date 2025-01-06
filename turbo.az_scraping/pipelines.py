# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime


class TurbobotPipeline:

    def process_item(self, item, spider):



        # column damaged
        adapter = ItemAdapter(item)

        # addin ID column
        value = adapter.get('url')
        adapter['ad_id'] = value.split("/")[-1].split("-")[0]

        # engine column splitting and cleaning
        value = adapter.get('engine')
        adapter['engine'] = float(value.split('/')[0].split(' ')[0])
        adapter['horsepower'] =  int(value.split('/')[1].split(' ')[1].strip())
        adapter['fuel_type'] = value.split('/')[2].strip()


        # number of views
        value = adapter.get('number_of_views')
        adapter['number_of_views'] = int(re.sub(r'\D', '', value))


        #Odometer km
        value = adapter.get('odometer_km')
        adapter['odometer_km'] = int(re.sub(r'\D', '', value))


        # price azn
        value = adapter.get('price_azn')
        if value is None:
            adapter['price_azn'] = adapter['price_original']
        value = adapter.get('price_azn')
        adapter['price_azn'] = int(re.sub(r'\D', '', value))


        # seats_count and year to int
        to_int = ['seats_count','year']
        for field_name in to_int:
            value = adapter.get(field_name)
            if value is not None:
                adapter[field_name] = int(value)


        # updated
        value = adapter.get('updated')
        adapter['updated'] = datetime.strptime(value.split(": ")[1], '%d.%m.%Y').date()


        # product extras
        value = adapter.get('product_extras')
        adapter['product_extras'] = ", ".join(value)

        return item

########################################


import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'togrul',
            password = '11235813',
            database = 'TurboAz'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
               CREATE TABLE IF NOT EXISTS AUTOS(
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    ad_id VARCHAR(20) NOT NULL,
                    url VARCHAR(255),
                    region VARCHAR(50),
                    make VARCHAR(50),
                    model VARCHAR(100),
                    year INTEGER,
                    category VARCHAR(100),
                    color VARCHAR(50),
                    engine FLOAT,
                    odometer_km INTEGER,
                    transmission VARCHAR(50),
                    gear VARCHAR(50),
                    is_new  VARCHAR(10),
                    seats_count INTEGER,
                    prior_owners_count VARCHAR(50),
                    auto_condition VARCHAR(200),
                    market VARCHAR(100),
                    vin VARCHAR(50),
                    description TEXT,
                    updated DATE,
                    number_of_views INTEGER,
                    price_original VARCHAR(50),
                    price_azn INTEGER,
                    status_order VARCHAR(50),
                    damaged VARCHAR(20),
                    product_extras TEXT,
                    horsepower INTEGER,
                    fuel_type VARCHAR(50),
                    UNIQUE (ad_id) )
                    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into AUTOS (
            ad_id,
            url,
            region,
            make,
            model,
            year,
            category,
            color,
            engine,
            odometer_km,
            transmission,
            gear,
            is_new,
            seats_count,
            prior_owners_count,
            auto_condition,
            market,
            vin,
            description,
            updated,
            number_of_views,
            price_original,
            price_azn,
            status_order,
            damaged,
            product_extras,
            horsepower,
            fuel_type
            ) values (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s) ON DUPLICATE KEY UPDATE
        url = VALUES(url),
        region = VALUES(region),
        make = VALUES(make),
        model = VALUES(model),
        year = VALUES(year),
        category = VALUES(category),
        color = VALUES(color),
        engine = VALUES(engine),
        odometer_km = VALUES(odometer_km),
        transmission = VALUES(transmission),
        gear = VALUES(gear),
        is_new = VALUES(is_new),
        seats_count = VALUES(seats_count),
        prior_owners_count = VALUES(prior_owners_count),
        auto_condition = VALUES(auto_condition),
        market = VALUES(market),
        vin = VALUES(vin),
        description = VALUES(description),
        updated = VALUES(updated),
        number_of_views = VALUES(number_of_views),
        price_original = VALUES(price_original),
        price_azn = VALUES(price_azn),
        status_order = VALUES(status_order),
        damaged = VALUES(damaged),
        product_extras = VALUES(product_extras),
        horsepower = VALUES(horsepower),
        fuel_type = VALUES(fuel_type)""",
           (item["ad_id"],
            item["url"],
            item["region"],
            item["make"],
            item["model"],
            item["year"],
            item["category"],
            item["color"],
            item["engine"],
            item["odometer_km"],
            item["transmission"],
            item["gear"],
            item["is_new"],
            item["seats_count"],
            item["prior_owners_count"],
            item["auto_condition"],
            item["market"],
            item["vin"],
            item["description"],
            item["updated"],
            item["number_of_views"],
            item["price_original"],
            item["price_azn"],
            item["status_order"],
            item["damaged"],
            item["product_extras"],
            item["horsepower"],
            item["fuel_type"]
        ))

        ## Execute insert of data into database
        self.conn.commit()


    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.conn.close()