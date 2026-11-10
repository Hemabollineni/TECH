import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

def test_search_results(setup):
    driver = setup
    
    wait = WebDriverWait(driver, 20)
    
    search_box = wait.until(    
        EC.presence_of_element_located(
            (By.ID, "twotabsearchtextbox")
        )
    )
    
    search_box.clear()
    search_box.send_keys("iPhone")

    # submit serach
    search_box.send_keys(Keys.ENTER)
    
    # it gives multiple results, so we need to wait for the search results to load
    results = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
        )
    )
    
    print("Total search results:", len(results))
    
    for result in results[:5]:
        title_elements = result.find_elements(
            By.CSS_SELECTOR, "h2 span"
        )

        # print("Title elements found:", len(title_elements))
        for title in title_elements:
            print("Title:", title.text)
            