import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os

def extract_coordinates(url):
    match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
    if match:
        lat, lng = match.groups()
        return float(lat), float(lng)
    return None, None

def scrape_places(search_query, language, driver):
    all_place_data = []

    # Open Google Maps with the specific search query and language
    driver.get(f"https://www.google.com/maps/search/{search_query}?hl={language}")

    # Allow the page to load
    time.sleep(30)

    # Scrape the place data
    places = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    for place in places:
        try:
            name = place.find_element(By.CLASS_NAME, "qBF1Pd").text
            rating = place.find_element(By.CLASS_NAME, "MW4etd").text
            reviews = place.find_element(By.CLASS_NAME, "UY7F9").text
            link_element = place.find_element(By.TAG_NAME, "a")
            url = link_element.get_attribute("href")
            
            lat, lng = extract_coordinates(url)

            all_place_data.append({
                "Place Name": name,
                "Star Rating": rating,
                "Reviews Count": reviews.strip('()').replace(',', ''),
                "Location (Latitude and Longitude)": f"{lat}, {lng}",
                "URL": url,
            })

        except Exception as e:
            print(f"Error: {e}")

    return all_place_data

def main():
    parser = argparse.ArgumentParser(description="Scrape data from Google Maps")
    parser.add_argument('--queries', nargs='+', default=["restaurants in New Cairo", "cafe in New Cairo"], help="Search queries to use")
    parser.add_argument('--languages', nargs='+', default=["en", "ar"], help="Languages to use for the search (en, ar)")
    parser.add_argument('--output', default="new_cairo_restaurants_and_cafes.xlsx", help="Output file name")
    args = parser.parse_args()

    all_place_data = []

    # Set up the Selenium WebDriver        
    chrome_options = Options()
    chrome_options.add_argument("--disable-application-cache")

    driver = webdriver.Chrome(options=chrome_options)

    for search_query in args.queries:
        for lang in args.languages:
            place_data = scrape_places(search_query, lang, driver)
            all_place_data.extend(place_data)

    driver.quit()

    new_df = pd.DataFrame(all_place_data)

    # Check if the file exists
    if os.path.exists(args.output):
        # Read the existing data
        existing_df = pd.read_excel(args.output)
        # Append new data
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df

    # Drop duplicates
    updated_df.drop_duplicates(subset='Location (Latitude and Longitude)', keep='first', inplace=True)

    # ensure data types
    updated_df['Star Rating'] = updated_df['Star Rating'].astype(float)
    updated_df['Reviews Count'] = updated_df['Reviews Count'].astype(int)
    
    # Save the updated DataFrame
    updated_df.to_excel(args.output, index=False)

    print(f"Data saved to {args.output}")

if __name__ == "__main__":
    main()
