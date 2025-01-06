# Turbo.az Car Listings Scraper

A Python Scrapy project that extracts car listings data from Turbo.az and stores it in a MySQL database.

## Features

- Scrapes detailed car listings including make, model, price, specifications and features
- Uses proxy rotation via ScrapeOps to avoid IP blocking
- Processes and cleans data through custom pipelines
- Stores data in MySQL database with duplicate handling
- Implements fake user agents and browser headers for request anonymization

## Requirements

- Python 3.x
- MySQL
- Required packages: scrapy, mysql-connector-python, scrapeops-scrapy-proxy-sdk

## Installation

1. Clone the repository
```bash
git clone [your-repo-url]
cd turboaz-scraper
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure MySQL database
- Create a database named 'TurboAz'
- Update database credentials in `pipelines.py`

4. Set up ScrapeOps
- Sign up at scrapeops.io
- Update your API key in `settings.py`

## Project Structure

- `spiders/turbospider.py`: Main spider for crawling Turbo.az
- `items.py`: Defines the structure of scraped data
- `pipelines.py`: Data processing and MySQL storage logic
- `middlewares.py`: Custom middleware for proxy and header rotation
- `settings.py`: Project configuration and settings

## Data Fields

The scraper collects the following information for each car listing:
- Basic info: make, model, year, category
- Technical specs: engine size, horsepower, fuel type
- Condition: mileage, damage status, prior owners
- Pricing: original price, price in AZN
- Additional: region, VIN, features, description

## Usage

Run the spider:
```bash
scrapy crawl turbospider
```

Data will be saved to both MySQL database and `carsdata.csv`.

## Notes

- Respects the website's robots.txt
- Implements retry mechanism for failed requests
- Uses fake browser headers and user agents for avoiding detection
- Handles duplicate entries in database using ON DUPLICATE KEY UPDATE
