
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("https://www.amazon.in")

print("Amazon opened")

# 1. Locate search box using ID
search1 = driver.find_element(
    By.ID,
    "twotabsearchtextbox"
)

print("ID locator:", search1.get_attribute("id"))

# 2. Locate search box using NAME
search2 = driver.find_element(
    By.NAME,
    "field-keywords"
)

print("NAME locator:", search2.get_attribute("name"))

# 3. Locate search box using CSS Selector
search3 = driver.find_element(
    By.CSS_SELECTOR,
    "#twotabsearchtextbox"
)

print("CSS locator:", search3.get_attribute("id"))

# 4. Locate search box using XPath
search4 = driver.find_element(
    By.XPATH,
    '//input[@id="twotabsearchtextbox"]'
)

print("XPATH locator:", search4.get_attribute("id"))

driver.quit()
