import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import traceback

def scrape_eurojackpot_results():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Navigate to the EuroJackpot website
    driver.get("https://www.eurojackpot.com/en/results-history")
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[formcontrolname='jahr']"))
    )
    
    # Dictionary to store all results
    all_results = []
    
    # Loop through each year
    year_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='jahr']"))
    years = [option.get_attribute('value') for option in year_select.options]
    # years = ['2016', '2015', '2014']
    for year in years:
        # Select the year
        year_select.select_by_value(year)
        time.sleep(1)  # Wait for date options to update
        
        # Get the dates for this year
        date_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='datum']"))
        dates = [option.get_attribute('value') for option in date_select.options]
        
        for date in dates:
            # Select the date
            date_select.select_by_value(date)
            time.sleep(1)  # Wait for results to update
            
            # Extract the winning numbers
            number_elements = driver.find_elements(By.CSS_SELECTOR, ".winning-number")
            
            if len(number_elements) >= 7:  # We expect 5 main numbers + 2 Euro numbers
                main_numbers = [elem.text for elem in number_elements[:5]]
                euro_numbers = [elem.text for elem in number_elements[5:7]]
                
                # Store the results
                result = {
                    'draw_date': date,
                    'main_numbers': ','.join(main_numbers),
                    'euro_numbers': ','.join(euro_numbers)
                }
                all_results.append(result)
                print(f"Scraped results for {date}: {main_numbers} + {euro_numbers}")
            
            # Refresh the date select element after each date to avoid stale element errors
            date_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='datum']"))
        
        # Refresh the year select element after each year to avoid stale element errors
        year_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='jahr']"))
    
    # Close the driver
    driver.quit()
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('eurojackpot_results.csv', index=False)
    print(f"Saved {len(all_results)} EuroJackpot results to eurojackpot_results.csv")
    
    return df

def process_year(year):
    max_year_retries = 3
    for year_attempt in range(max_year_retries):
        try:
            # Initialize a new driver for each year
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.set_page_load_timeout(60)  # Increased timeout
            
            # Navigate to the EuroJackpot website
            driver.get("https://www.eurojackpot.com/en/results-history")
            
            # Wait for the page to load
            WebDriverWait(driver, 30).until(  # Increased wait time
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[formcontrolname='jahr']"))
            )
            
            # Select the year
            year_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='jahr']"))
            year_select.select_by_value(year)
            time.sleep(3)  # Increased wait time
            
            # Get the dates for this year
            date_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='datum']"))
            dates = [option.get_attribute('value') for option in date_select.options]
            
            year_results = []
            for date in dates:
                # Select the date
                date_select.select_by_value(date)
                time.sleep(1)  # Wait for results to update
                
                # Extract the winning numbers
                number_elements = driver.find_elements(By.CSS_SELECTOR, ".winning-number")
                
                if len(number_elements) >= 7:  # We expect 5 main numbers + 2 Euro numbers
                    main_numbers = [elem.text for elem in number_elements[:5]]
                    euro_numbers = [elem.text for elem in number_elements[5:7]]
                    
                    # Store the results
                    result = {
                        'draw_date': date,
                        'main_numbers': ','.join(main_numbers),
                        'euro_numbers': ','.join(euro_numbers)
                    }
                    year_results.append(result)
                    print(f"Scraped results for {date}: {main_numbers} + {euro_numbers}")
                
                # Refresh the date select element after each date to avoid stale element errors
                date_select = Select(driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='datum']"))
            
            return year_results
            
        except Exception as e:
            print(f"Error processing year {year} (attempt {year_attempt+1}/{max_year_retries}): {str(e)}")
            traceback.print_exc()
            try:
                driver.quit()
            except:
                pass
            
            if year_attempt < max_year_retries - 1:
                print(f"Retrying year {year} in 10 seconds...")
                time.sleep(10)  # Wait before retrying
            else:
                print(f"Failed to process year {year} after {max_year_retries} attempts")
                return []

if __name__ == "__main__":
    scrape_eurojackpot_results()
