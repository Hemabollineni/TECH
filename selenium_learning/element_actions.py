
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.amazon.in")

print("Page title:", driver.title)
print("Current URL:", driver.current_url)

# Wait up to 20 seconds for the search box
wait = WebDriverWait(driver, 20)

search_box = wait.until(
    EC.element_to_be_clickable(
        (By.ID, "twotabsearchtextbox")
    )
)

# Example 1: Enter iPhone
search_box.send_keys("iPhone")

print("Entered:", search_box.get_attribute("value"))

# Clear the search box
search_box.clear()

print("Search box cleared")

# Example 2: Enter Samsung
search_box.send_keys("Samsung")

print("Entered:", search_box.get_attribute("value"))

# Submit search
search_box.send_keys(Keys.ENTER)

print("Samsung search submitted")

# Wait for search results
wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
    )
)

print("Search results loaded!")

driver.quit()
