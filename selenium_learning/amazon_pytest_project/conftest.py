import pytest 
from selenium import webdriver 

@pytest.fixture
def setup(): 
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in")
    yield driver
    
    driver.quit()