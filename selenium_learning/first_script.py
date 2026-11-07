from selenium import webdriver
import time

driver = webdriver.Chrome()

print("Chrome opened successfully")

driver.get("https://www.google.com")

print("Website Title:", driver.title)

print("Current URL:", driver.current_url)

# Keep browser open for 10 seconds
time.sleep(10)

driver.quit()

print("Browser closed")