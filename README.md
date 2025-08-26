# Amazon Web Scraper

This Python script, part of our ongoing 'Data Analysis Series' scrapes product data from Amazon India (https://www.amazon.in) for a given keyword or a specific product URL and saves the results to a CSV file (amazon_products.csv). The script collects details such as product title, price, rating, reviews, availability, features, description, ASIN, image URLs, and timestamp.

## Features

- Scrapes product details from Amazon India search results or a single product page.
- Handles retries for failed requests and detects CAPTCHAs.
- Saves scraped data to a CSV file with proper formatting.
- Includes error handling for robust scraping.
- Limits the number of products scraped to avoid rate-limiting issues.

### Requirements

- Python 3.6+
- Required libraries: `pip install requests beautifulsoup4`
- A stable internet connection to access Amazon India.

### Installation

- Clone or download this repository to your local machine.
- Navigate to the project directory:cd path/to/your/project
- Install the required Python libraries: `pip install requests beautifulsoup4`
- Ensure your project directory has write permissions to create the output CSV file.

### Usage
- Open AmazonWebscraping.py in a text editor (e.g., VS Code).
- Modify the keyword (e.g., "data analyst t shirts") or single_url in the if __name__ == '__main__': block to scrape different products.
- Adjust max_pages (default: 2) or max_products (default: 30) in the scrape_amazon function to control the number of search result pages or products scraped.


### Run the Script
Open a terminal in VS Code or your preferred command-line tool.
Navigate to the project directory:cd C:\Users\hp\python programming journey
Run the script: `python AmazonWebscraping.py`


## Working
- Scrape a single product (default: https://www.amazon.in/Seek-Buy-Love-Spreadsheet-Accountant/dp/B0CZJ82YT1).
- Search for products matching the keyword (default: "data analyst t shirts") and scrape up to 30 products across 2 pages.
- Save results to amazon_products.csv in the project directory.


### Check the Output
The script generates amazon_products.csv in C:\Users\hp\python programming journey.
Open the CSV in:
VS Code: Double-click amazon_products.csv in the File Explorer. Install the Rainbow CSV or Excel Viewer extension for better formatting.
Excel: Double-click the file in File Explorer to open it as a spreadsheet.
Google Sheets: Upload the file to Google Drive and open with Google Sheets.



## Dataset Schema
The script produces amazon_products.csv with the following columns:

| Column Name   | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **asin**      | Amazon Standard Identification Number.                                      |
| **url**       | Product page URL.                                                           |
| **title**     | Product title.                                                              |
| **price**     | Product price in INR.                                                       |
| **currency**  | Currency (fixed as INR).                                                    |
| **rating**    | Star rating (e.g., 4.3).                                                    |
| **rating_count** | Number of customer reviews.                                              |
| **availability** | Stock status (e.g., "In stock").                                         |
| **bullets**   | Product features (bullet points, joined by `|`).                            |
| **description** | Product description (truncated to 2000 characters).                       |
| **image_urls** | Up to 5 product image URLs (joined by `;`).                                |
| **timestamp** | UTC timestamp of when the data was scraped.                                 |


## Troubleshooting
- CSV File Not Found:
- Ensure the script ran successfully and check C:\Users\hp\python programming journey for amazon_products.csv.
- Run VS Code as Administrator if write permissions are an issue.
- Missing or Incomplete Data:

If the CSV has fewer rows than expected, check the terminal output for errors (e.g., "Could not scrape" or "CAPTCHA detected").
Increase sleep times in find_product_urls or scrape_amazon (e.g., random.uniform(8.0, 12.0)) to avoid CAPTCHAs.
Verify selectors in get_product_title, get_product_price, etc., match Amazon’s current HTML structure.


## Example Output
Running the script with default settings produces output like:
Saved single product to csv
Searching for 'data analyst t shirts'...
Found 10 products
Scraping product 1/10: https://www.amazon.in/Computer-Loading-Graphic-T-Shirt-Regular/dp/B0DYF458N4
Scraping product 2/10: https://www.amazon.in/Seek-Buy-Love-Spreadsheet-Accountant/dp/B0CZJ82YT1
...

The resulting amazon_products.csv contains up to 31 rows (1 single product + up to 30 search results).

## License
This project is for educational purposes. Ensure compliance with Amazon’s terms of service when scraping.

## Contributing
Feel free to submit issues or pull requests for improvements, such as adding new fields, handling more edge cases, or visualizing scraped data.

## Author

Made by Hashir khan   
Feel free to ⭐ the repo if you found it helpful!
