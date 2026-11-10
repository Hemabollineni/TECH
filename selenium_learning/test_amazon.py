
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in")

    yield driver

    driver.quit()


# Test 1: Amazon Homepage
def test_amazon_home(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    wait.until(EC.title_contains("Amazon"))

    print("Homepage title:", driver.title)

    assert "Amazon" in driver.title

    print("Amazon homepage verified successfully")


# Test 2: Amazon Search
def test_amazon_search(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "twotabsearchtextbox")
        )
    )

    search_box.clear()
    search_box.send_keys("iPhone")
    search_box.send_keys(Keys.ENTER)

    results = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
        )
    )

    product_titles = []

    for result in results[:5]:
        title_elements = result.find_elements(
            By.CSS_SELECTOR, "h2[aria-label] span"
        )

        for title in title_elements:
            if title.text.strip():
                product_titles.append(title.text.strip())
                print("Product:", title.text)

    assert len(product_titles) > 0
    assert any(
        "iphone" in title.lower()
        for title in product_titles
    )

    print("Amazon search verified successfully")


# Test 3: Accounts & Lists Dropdown
def test_accounts_dropdown(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    accounts_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "nav-link-accountList")
        )
    )

    ActionChains(driver).move_to_element(
        accounts_dropdown
    ).perform()

    flyout = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "nav-flyout-accountList")
        )
    )

    assert flyout.is_displayed()

    print("Accounts dropdown is visible")

    menu_items = driver.find_elements(
        By.CSS_SELECTOR,
        "#nav-al-container ul li a.nav-link.nav-item"
    )

    actual_items = [item.text for item in menu_items]

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
        "Register for a free Business Account"
    ]

    print("Total menu items:", len(actual_items))

    assert len(actual_items) > 0

    for expected_item in expected_items:
        assert expected_item in actual_items
        print("Verified:", expected_item)

    print("Accounts dropdown verified successfully")


# Test 4: Language Dropdown
def test_language_dropdown(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    language_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "icp-nav-flyout")
        )
    )

    ActionChains(driver).move_to_element(
        language_dropdown
    ).perform()

    flyout = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "nav-flyout-icp")
        )
    )

    assert flyout.is_displayed()

    print("Language dropdown is visible")

    actual_languages = [
        item.get_attribute("lang")
        for item in driver.find_elements(
            By.CSS_SELECTOR,
            "#nav-flyout-icp ul li a.nav-link"
        )
    ]

    for language in actual_languages:
        print("Language option:", language)

    print("Total language options:", len(actual_languages))

    expected_languages = [
        "en-IN",
        "hi-IN",
        "ta-IN",
        "te-IN",
        "kn-IN",
        "ml-IN",
        "bn-IN",
        "mr-IN"
    ]

    assert len(actual_languages) == 8
    assert actual_languages == expected_languages

    print("All 8 language options verified successfully")
