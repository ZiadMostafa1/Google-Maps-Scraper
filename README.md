# Google Maps Scraper

## Description

This project is a Python script that scrapes place data from Google Maps using Selenium. It retrieves information about places based on search queries and languages, including place names, star ratings, review counts, and geographical coordinates. The data is then saved to an Excel file.

## Features

- Scrapes data for multiple search queries and languages.
- Extracts place name, star rating, review count, and location coordinates.
- Saves the data to an Excel file, appending new data to existing files if present.
- Handles duplicates and ensures correct data types for ratings and reviews.

## Requirements

- Python 3.x
- Selenium
- pandas
- openpyxl (for Excel file handling)
- Chrome WebDriver

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ZiadMostafa1/Google-Maps-Scraper
   cd google-maps-scraper
   ```

2. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download and set up Chrome WebDriver:** (if needed)
   - Download the WebDriver from [ChromeDriver](https://sites.google.com/chromium.org/driver/).
   - Ensure the WebDriver executable is in your system's PATH or specify its location in the script.

## Usage

Run the script with the desired search queries and languages:

```bash
python scraper.py --queries "restaurants in New Cairo" "cafe in New Cairo" --languages en ar --output new_cairo_restaurants_and_cafes.xlsx
```

### Arguments

- `--queries`: A list of search queries to use (e.g., "restaurants in New Cairo").
- `--languages`: A list of languages to use for the search (e.g., "en" for English, "ar" for Arabic).
- `--output`: The name of the output Excel file (default is `new_cairo_restaurants_and_cafes.xlsx`).

## Notes

- The script uses time.sleep(30) to allow the page to load. Adjust the sleep time if necessary based on your internet speed and page loading times.
- The script is designed for Google Maps' current HTML structure. If Google Maps updates its layout, you may need to adjust the class names and elements used for scraping.