
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.selenium.dev/")

wait = WebDriverWait(driver, 15)

print("Page title:", driver.title)

# Find GET STARTED link
link = wait.until(
    EC.element_to_be_clickable(
        (By.LINK_TEXT, "GET STARTED")
    )
)

# Read link text
print("Link text:", link.text)

# Click the link
link.click()

# Print destination URL
print("Current URL:", driver.current_url)

driver.quit()
