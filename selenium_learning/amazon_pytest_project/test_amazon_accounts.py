# import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_accounts_dropdown(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)
    
    # checks whether the element exists and is visible
    accounts_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "nav-link-accountList")
        )
    )
    
    ActionChains(driver).move_to_element(accounts_dropdown).perform()
    # time.sleep(3)
    
    print("Mouse hovered over Accounts & Lists")
    
    flyout = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "nav-flyout-accountList")
        )
    )
    
    assert flyout.is_displayed()
    print("Accounts dropdown is visible")
    
    menu_items = driver.find_elements(
        By.CSS_SELECTOR, "#nav-al-container ul li a.nav-link.nav-item"
    )

    expected_items = [
        "Create a Wish List",
        "Wish from Any Website",
        "Baby Wishlist",
        "Discover Your Style",
        "Explore Showroom", 
        "Your Account",
        "Your Orders",
        "Your Wish List",
        "Keep shopping for",
        "Your Recommendations",
        "Your Prime Membership",
        "Your Prime Video",
        "Your Subscribe & Save Items",
        "Memberships & Subscriptions",   
        "Your Seller Account",
        "Manage Your Content and Devices",
        "Your Music Library",
        "Register for a free Business Account",
    ]
    
    
    # print("Total menu items:", len(menu_items))
    assert len(menu_items) > 0
    
    actual_items = [item.text for item in menu_items]

    for expected_item in expected_items:
        assert expected_item in actual_items
        print("Verified:", expected_item)
          