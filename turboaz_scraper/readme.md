# Turbo.az Car Listings Scraper

## Project Overview

This Python-based web scraping project extracts detailed car listing information from Turbo.az, Azerbaijan's leading automotive marketplace. The scraper is built using the Scrapy framework and implements various techniques to ensure reliable data collection while respecting the website's resources. The collected data is processed, cleaned, and stored in a MySQL database for further analysis.

## Key Features

### Web Scraping Capabilities
- Systematically crawls through car listings on Turbo.az
- Extracts comprehensive vehicle information including specifications, pricing, and features
- Handles pagination automatically to collect data from multiple pages
- Implements proper error handling and retry mechanisms

### Anti-Ban Measures
- Integrates with ScrapeOps proxy service for IP rotation
- Implements random user agent rotation to mimic different browsers
- Uses realistic browser headers to avoid detection
- Configurable request delays to prevent server overload

### Data Processing
- Robust data cleaning pipeline for consistent formatting
- Converts text data to appropriate numerical types
- Handles missing or malformed data gracefully
- Standardizes date formats and numerical values
- Processes multilingual content (Azerbaijani and Russian)

### Data Storage
- Stores data in a structured MySQL database
- Implements efficient duplicate handling
- Updates existing records when re-scraping
- Maintains data integrity through proper schema design

## Technical Architecture

### Spider Component (`spiders/turbospider.py`)
The spider is responsible for:
- Navigating through the website's structure
- Extracting raw data from HTML elements
- Managing the crawling process
- Handling pagination and following links

### Item Definition (`items.py`)
Defines the data structure with fields including:
- Vehicle identification (ad_id, VIN)
- Basic information (make, model, year)
- Technical specifications (engine, transmission, fuel type)
- Condition details (mileage, damage status)
- Market information (price, location)

### Data Processing Pipeline (`pipelines.py`)
Two main pipeline stages:
1. `TurbobotPipeline`: Data cleaning and transformation
   - Extracts numerical values from text
   - Standardizes formats
   - Processes complex fields (engine specifications, dates)
   
2. `SaveToMySQLPipeline`: Database operations
   - Manages database connections
   - Handles data insertion and updates
   - Implements duplicate checking

### Middleware Configuration (`middlewares.py`)
Contains custom middleware classes for:
- ScrapeOps proxy integration
- User agent rotation
- Browser header management
- Request/response processing

## Setup Instructions

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-username/turboaz_scraper.git
cd turboaz_scraper

# Create a virtual environment (recommended)
# This keeps our project dependencies isolated from other Python projects
python -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install all required dependencies from requirements.txt
# This will install Scrapy, MySQL connector, and other necessary packages
pip install -r requirements.txt
```

### 2. Database Configuration
```sql
-- Create database
CREATE DATABASE TurboAz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges (adjust username and password)
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON TurboAz.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```

Update database credentials in `pipelines.py`:
```python
self.conn = mysql.connector.connect(
    host = 'localhost',
    user = 'your_username',
    password = 'your_password',
    database = 'TurboAz'
)
```

### 3. ScrapeOps Configuration
1. Sign up at [ScrapeOps](https://scrapeops.io)
2. Obtain your API key
3. Update `settings.py` with your key:
```python
SCRAPEOPS_API_KEY = 'your_api_key'
```

### 4. Project Configuration
Adjust settings in `settings.py` based on your needs:
```python
# Crawling speed
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 16

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 3

# Output settings
FEEDS = {
    'carsdata.csv': {'format': 'csv'}
}
```

## Usage

### Running the Scraper
```bash
# Make sure you're in the turboaz_scraper directory
cd turboaz_scraper

# Basic run command
scrapy crawl turbospider

# For debugging or seeing more detailed output
scrapy crawl turbospider --loglevel=DEBUG
```

### Monitoring Progress
The scraper provides console output showing:
- Pages processed
- Items scraped
- Error rates
- Processing speed

### Database Management
The MySQL database automatically:
- Creates required tables on first run
- Updates existing records based on ad_id
- Maintains data consistency

## Error Handling and Logging

The scraper implements comprehensive error handling:
- Retries failed requests
- Logs errors for debugging
- Maintains scraping progress on failures
- Provides detailed error messages

## Best Practices and Limitations

### Ethical Scraping Guidelines
- Respect robots.txt directives
- Implement reasonable delays
- Monitor server response codes
- Limit concurrent requests

### Known Limitations
- Site structure changes may require updates
- Some fields may be missing in listings
- Language variations can affect parsing
- Proxy service availability dependent
