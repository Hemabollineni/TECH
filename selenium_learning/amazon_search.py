
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# 1. Open Chrome
driver = webdriver.Chrome()

# 2. Maximize browser
driver.maximize_window()

# 3. Open Amazon India
driver.get("https://www.amazon.in")

print("Amazon opened successfully")

# 4. Wait until search box is available
wait = WebDriverWait(driver, 15)

search_box = wait.until(
    EC.element_to_be_clickable(
        (By.ID, "twotabsearchtextbox")
    )
)

# 5. Enter iPhone in search box
search_box.send_keys("iPhone")

# 6. Press Enter
search_box.send_keys(Keys.ENTER)

print("Searching for iPhone...")

# 7. Wait for search results
wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
    )
)

print("Search results loaded!")

# 8. Keep browser open
time.sleep(15)

# 9. Close browser
driver.quit()
