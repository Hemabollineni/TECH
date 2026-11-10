from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://www.swiggy.com/")

driver.maximize_window()

wait = WebDriverWait(driver, 20)

signin = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[text()='Sign in']")
    )
)

signin.click()