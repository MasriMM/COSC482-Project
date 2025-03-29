from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
import time
import chromedriver_autoinstaller 

print("Setting up driver")
options = Options() 
options.add_argument("--headless")  
options.add_argument("--disable-gpu")  
options.add_argument("--window-size=1920x1080")  
options.add_argument("--disable-blink-features=AutomationControlled")  

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=options)

try:
    driver.get('https://www.momondo.com/flights')
    
    # Wait for elements to load
    wait = WebDriverWait(driver, 10)

    print("Selecting origin field (Paris)...")
    origin_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Flight origin input']")))
    driver.execute_script("arguments[0].value = '';", origin_field)
    origin_field.send_keys('Paris')
    time.sleep(3)
    origin_field.send_keys(Keys.ARROW_DOWN)
    origin_field.send_keys(Keys.RETURN)

    print("Selecting destination field (Beirut)...")
    destination_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Flight destination input']")))
    driver.execute_script("arguments[0].value = '';", destination_field)
    destination_field.send_keys('Beirut')
    time.sleep(3)
    destination_field.send_keys(Keys.ARROW_DOWN)
    destination_field.send_keys(Keys.RETURN)
    
    print("Selecting check-in date...")
    checkin_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Departure']")))
    checkin_field.click()
    time.sleep(2)
    print('in: dec 1')
    while True:
        try:
            checkin_date = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, 'December 1, 2025')]")))
            checkin_date.click()
            break  # Stop if found
        except:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next month']")))
            next_button.click()
            time.sleep(1)
    print('out: dec 31')
    checkout_date = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'December 31, 2025')]")))
    checkout_date.click()

    # Clicking the date selection button 
    try:
        select_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dialog-footer-button')]")))
        select_button.click()
    except:
        print("Select button not found, continuing...")

    # Clicking the search button
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search']")))
    search_button.click()

    time.sleep(5)  # Wait for results to load
    
    url = driver.current_url
    driver.get(url)
    # Scraping ticket prices
    ticket_price_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'price-text')]")))
    prices = [price.text for price in ticket_price_elements]

    print("Ticket Prices:", prices)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
