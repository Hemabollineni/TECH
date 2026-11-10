from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_language_dropdown(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)
    
    language_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "icp-nav-flyout")
        )
    )
    
    ActionChains(driver).move_to_element(language_dropdown).perform()
     
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
            By.CSS_SELECTOR, "#nav-flyout-icp ul li a.nav-link"
        )
    ]
    
    for item in actual_languages:
        print("Language option:", item)
    
    print("Total language options:", len(actual_languages))
    assert len(actual_languages) > 0

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

    assert actual_languages == expected_languages

    print("All 8 language options verified successfully")