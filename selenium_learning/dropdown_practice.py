
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://the-internet.herokuapp.com/dropdown")

wait = WebDriverWait(driver, 15)

# Locate dropdown
dropdown_element = wait.until(
    EC.presence_of_element_located(
        (By.ID, "dropdown")
    )
)

# Create Select object
dropdown = Select(dropdown_element)

# Example 1: Select by visible text
dropdown.select_by_visible_text("Option 1")
print("Selected:", dropdown.first_selected_option.text)

# Example 2: Select by value
dropdown.select_by_value("2")
print("Selected:", dropdown.first_selected_option.text)

driver.quit()
