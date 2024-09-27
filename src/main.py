from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
from urllib.request import Request, urlopen
import json
import ssl
import urllib

driver = webdriver.Chrome()
driver.get("https://www.ubereats.com/ca/city/london-on")
driver.refresh()
print("Page loaded and refreshed")

try:
    # Wait for the address input field
    wait = WebDriverWait(driver, 2)  
    address_input = wait.until(EC.element_to_be_clickable((By.ID, "location-typeahead-home-input")))
    print("Found address input field")
    # Clear any existing text and enter the address
    address_input.clear()
    # address_input.send_keys(input("Please enter your location: "))
    address_input.send_keys("811 sarnia rd")
    print("Entered address")
    # Submit the address
    time.sleep(2)
    address_input.send_keys(Keys.RETURN)
    print("Submitted address")
    # Wait for the page to update and restaurant listings to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))  # No timeout parameter here
    print("Page updated with restaurant listings")
    
    
    time.sleep(2)
    offers_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Offers']"))).click()
    
    time.sleep(2)
    sort_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Sort']"))).click()
    
    time.sleep(2)
    delivery_time_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='  Delivery time']"))).click()
    print("Delivery time button clicked")

    time.sleep(5)
    apply_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Apply']"))).click()
    print("Apply button clicked")
    time.sleep(2)
    show_more_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Show more']"))).click()
    print("Show more button clicked")
    time.sleep(2)
    # Get the page source
    html = driver.page_source
    print("Got page source")
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    restaurant_containers = soup.find_all('div', attrs={"data-testid": "store-card"})
    restaurant_data = []

    if restaurant_containers:
        print("Found restaurant listings:")
        for container in restaurant_containers:
            # Look for the offer text directly
            offer_text = container.find(string=lambda text: text and ("Buy 1, Get 1 Free" in text or "Offers Available" in text))
            
            if offer_text:
                # Extract restaurant name
                restaurant_name = container.find('h3').text if container.find('h3') else "Unknown"
                offer = offer_text.strip()
                
                print(f"Restaurant: {restaurant_name}")
                print(f"Offer: {offer}")
                print("---")
                
                restaurant_data.append({
                    "name": restaurant_name,
                    "offer": offer
                })
    else:
        print("No restaurant listings found")

    # Print the collected data
    print("\nCollected Restaurant Data:")
    print(json.dumps(restaurant_data, indent=4))

    # Dump the data to a JSON file
    with open('restaurant_offers.json', 'w', encoding='utf-8') as out:
        json.dump(restaurant_data, out, indent=4, ensure_ascii=False)
    
    print(f"\nData has been saved to 'restaurant_offers.json'")


except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    input("Press Enter to close the browser...")
    driver.quit()
    print("Browser closed")
    
    
    
    #TODO: implement the commented out stuff above
    
