from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

# Set Chrome options
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Run in headless mode for Colab
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Automatically install the correct ChromeDriver version
chromedriver_autoinstaller.install()

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Open Momondo Flight Search Page (RUH to Beirut)
url = "https://www.momondo.com/flight-search/RUH-BEY/2025-12-01/2026-02-28?ucs=1xdidg9&sort=bestflight_a"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Function to get prices
def get_prices():
    prices = driver.find_elements(By.CLASS_NAME, "f8F1-price-text")
    price_list = []
    for price in prices:
        price_text = price.text
        if price_text:
            price_list.append({'Price': price_text})
    return price_list

# Get initial set of prices
price_list = get_prices()

# Try to click the "Show More" button if it exists (limited to 3 times)
for i in range(3):
    try:
        # Locate the "Show More Results" button
        show_more_button = driver.find_element(By.CLASS_NAME, "show-more-button")

        # Scroll to the button and click
        ActionChains(driver).move_to_element(show_more_button).click().perform()

        # Wait for more results to load
        time.sleep(5)

        # Get new prices after clicking "Show More"
        price_list.extend(get_prices())

        print(f"Clicked 'Show More' {i} time(s)")

    except Exception as e:
        print("No more results button found or scraping failed:", e)
        break

# Close the browser
driver.quit()

# Save the results to a CSV file
df = pd.DataFrame(price_list, columns=["Price"])
df.to_csv("RUH_to_BEI_momondo_prices.csv", index=False)  # Save to a CSV file in Colab
print(df)
print("Scraping completed! Prices saved in RUH_to_BEI_momondo_prices.csv")