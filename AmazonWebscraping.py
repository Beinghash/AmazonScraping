# Import neccessary libraries 
import requests 
from bs4 import BeautifulSoup
import random
import csv
import time 
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

# headers to make our request look like real browser 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # Set browser like user agent
    "Accept-Language": "en-US,en;q=0.9",  # Set preferred language to english
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  # Specify accepted content types
    "Referer": "https://www.amazon.in/",  # Set referer to Amazon homepage
    "Connection": "keep-alive"  # Keep connection alive for better session handling
}

# Function to fetch webpage content with retries
def get_page_content(url, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=20)  # Send HTTP GET request
            if response.status_code == 200:  # Handle 200 status code (healthy connection)
                if 'Robot Check' in response.text or 'captcha' in response.text.lower():
                    print(f'Captcha detected at {url}! please try again later or by using different browser')
                    return None  # return none if captcha detected
                return BeautifulSoup(response.text, 'html.parser')   # else parse html content
            else:  # Handle non-200 status code (unhealthy connection) [eg: 404 error]
                print(f'Failed to parse webpage at {url} status code: {response.status_code} attempt: {attempt}/{max_retries}')
                if attempt == max_retries:
                    return None # return none if all entries reached are failed 
        except Exception as e:
            if attempt == max_retries:
                return None    # return none if all entries are reached 
        time.sleep(random.uniform(3.0, 6.0) * attempt)  # Wait longer with each retry (exponential backoff) in seconds 
    return None     # return none if all retries failed     

# Function to clean the text
def clean_text(text):
    if not text:
        return ''  # Return empty string if no text
    return ' '.join(text.split()).strip() # join and split and strip any extra spaces or new lines 

# Function to get product title 
def get_product_title(soup):
    title = soup.find('span', id='productTitle')    # find the 'product title' in a span with the given class
    return clean_text(title.text) if title else ''  # return cleaned title text else empty string if not found 

# Function to get product price 
def get_product_price(soup):
    price = soup.find('span', class_='a-offscreen')  # find the 'price' in a span with the given class
    if not price:   # Check if primary price selector failed 
        price = soup.find('span', class_='priceblock_ourprice')  # try fall back price selector 
    return clean_text(price.text) if price else ''  # return cleaned price text else empty string if not found 

# Function to get product rating 
def get_product_rating(soup):
    rating = soup.find('span', class_='a-icon-alt')   # find the 'product rating' in a span with the given class
    if rating:
        text = clean_text(rating.text) # clean the rating text 
        try:
            return float(text.split()[0]) # Extract and convert first word to float (eg: 4.3)
        except:
            return None
    return None    # return none if rating element not found     

# Function to get number of reviews
def get_product_reviews(soup):
    reviews = soup.find('span', id='acrCustomerReviewText') # find 'product reviews' in a span with given id
    if reviews:
        text = clean_text(reviews.text)  # Clean the reviews 
        try:
            return int(text.split()[0].replace(',', '')) # Extract number, remove commas and convert to int 
        except:
            return None
    return None    

# Function to get product features 
def get_product_bullets(soup):
    bullet_list = soup.find('div', id='feature-bullets')    # find 'product features' in a div with given id
    if bullet_list:
        bullets = bullet_list.find_all('span', class_='a-list-item')  # find all span elements with given class
        return ' | '.join(clean_text(bullets.text) for bullet in bullets if bullet.text.strip())  # return joined clean bullet text with ' | '
    else:
        return ''  # Return empty string if no bullets are found

# Function to get product Description
def get_product_description(soup):
    description = soup.find('div', id='productDescription')  # find 'Product Description' in a div with given id
    if description:
        return clean_text(description.text)[:2000]  # retun clean description and limit to 5000 characters  
    else:
        return '' # Return empty string if no description is found

# Function to get product ASIN (Amazon Standard Identification Number)    
def get_product_asin(url, soup):
    asin_input = soup.find('input', id='ASIN') # find input element with id asin
    if asin_input and asin_input.get('value'): # Check if asin exists and if it has any value 
        return asin_input['value'].strip()     # return clean asin value 
    parts = url.split('/dp/') #Split URL at '/dp/' to find ASIN
    if len(parts) > 1:   # Check if URL contains '/dp/'
        return parts[1].split('/')[0]   # Extract ASIN from url
    return '' # Return empty string if ASIN not found

def get_product_availability(soup):
    availability = soup.find('div', id='availability') # find 'availability' in a div with given id
    return clean_text(availability.text) if availability else '' # return cleaned 'availability' else empty string if not found 

# Function to get product image URLs
def get_product_images(soup):
    images = soup.find_all('img', src=True)       # find all img tags with src attribute
    image_urls = []
    for img in images:
        src = img['src']
        if 'SL' in src:           # Check if image is a product image (contains 'SL')
            image_urls.append(src)
    return ';'.join(image_urls[:5])     # join upto 5 image urls with ';'

# Function to scrape a single product   
def scrape_product(url):  
    soup = get_page_content(url)      # get webpage content as BeautifulSoup oject 
    if not soup:
        print(f'Could not scrape {url}')
        return None
    # Creating dictionaries to store product details    
    product = {
        'asin': get_product_asin(url, soup),
        'url': url,
        'title': get_product_title(soup),
        'price': get_product_price(soup),
        'currency': 'INR',
        'rating' : get_product_rating(soup),
        'rating_count':get_product_reviews(soup),
        'availability': get_product_availability(soup),
        'bullets': get_product_bullets(soup),
        'description': get_product_description(soup),
        'image_urls': get_product_images(soup),
        'timestamp': datetime.utcnow().isoformat()   # Recording current timestamp
    }
    return product             # return product dictionary

# Function to save products to csv 
def save_to_csv(products, filename='amazon_products.csv'):
    fieldnames = ['asin', 'url', 'title', 'price', 'currency', 'rating', 'rating_count',
                  'availability','bullets', 'description', 'image_urls', 'timestamp']   # Define CSV column names 
    with open(filename, 'a', newline='', encoding='utf-8') as f:  # Open CSV file in append mode      
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # Creating of CSV Writer
        if f.tell() == 0:   # Check if file is empty at start
            writer.writeheader()   # Write CSV header 
        for product in products:
            writer.writerow(product)    # Write product data to CSV

# Function to find products urls
def find_product_urls(keyword, max_pages=2, max_products=30):
    product_urls = []   # Initialize list for product urls 
    base_url = 'https://www.amazon.in' 
    for page in range(1, max_pages+1):
        search_url = f'{base_url}/s?k={keyword.replace(' ','+')}&page={page}' # Build search url with keyword and page number 
        soup = get_page_content(search_url) # Get search page content
        if not soup:
            print(f'Failed to load search page {page}')
            continue   # Skip to next page if failed
        links = soup.find_all('a', class_='a-link-normal s-no-outline')    # Find all product links
        for link in links:
            href = link.get('href','')   # Get href attribute of link 
            if '/dp/' in href and not href.startswith('http'):   # Check if link is a product URL (relative URL)
                full_url = base_url + href.split('?')[0]    # Build full product url
                if full_url not in product_urls and full_url.startswith(base_url):
                    product_urls.append(full_url)    # Add url to list
            if len(product_urls) >= max_products:     # Stop if max_products reached 
                return product_urls
        time.sleep(random.uniform(5.0, 8.0))    # Wait 5-8 seconds before next page 
    return product_urls[:max_products]       # Return limited list of product urls 

# Function to scrape amazon
def scrape_amazon(keyword, max_pages=2, max_products=30):     # Add max_products parameter
    print(f"Searching for '{keyword}'...")
    product_urls = find_product_urls(keyword, max_pages, max_products)   # Pass max_products
    print(f'Found {len(product_urls)} products')
    products = []
    for i, url in enumerate(product_urls, 1):
        print(f'Scraping product {i}/{len(product_urls)}: {url}')
        product = scrape_product(url)
        if product:
            products.append(product)
        if len(products) >= 5:
            save_to_csv(products)
            products = []
        time.sleep(random.uniform(5.0, 8.0))
    if products:
        save_to_csv(products)            

# Main 
if __name__ == '__main__':
    # Scrape single product
    single_url = 'https://www.amazon.in/Seek-Buy-Love-Spreadsheet-Accountant/dp/B0CZJ82YT1?th=1&psc=1'
    product = scrape_product(single_url)
    if product:
        save_to_csv([product])
        print('Saved single product to csv')
    # Scrape multiple products for a keyword     
    scrape_amazon(keyword='data analyst t shirts', max_pages=2, max_products=30)    
