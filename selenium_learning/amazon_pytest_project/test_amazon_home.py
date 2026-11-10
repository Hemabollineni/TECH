import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_amazon_home(setup):
    
    driver = setup
    assert "amazon.in" in driver.title.lower()
    print(driver.title)

    wait = WebDriverWait(driver, 20)
    
    wait.until(
        EC.presence_of_element_located(
            (By.ID, "twotabsearchtextbox")
        )
            
    )   
