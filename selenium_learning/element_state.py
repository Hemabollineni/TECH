
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://the-internet.herokuapp.com/checkboxes")

wait = WebDriverWait(driver, 15)

checkboxes = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "input[type='checkbox']")
    )
)

# Check initial states
print("Before clicking:")
print("Checkbox 1:", checkboxes[0].is_selected())
print("Checkbox 2:", checkboxes[1].is_selected())

# Click first checkbox
checkboxes[0].click()

# Click second checkbox
checkboxes[1].click()

# Check updated states
print("\nAfter clicking:")
print("Checkbox 1:", checkboxes[0].is_selected())
print("Checkbox 2:", checkboxes[1].is_selected())

driver.quit()
