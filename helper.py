import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import REWARD_URL

def try_with_retry(action_func, max_attempts=3):
    """Try the function with a set number of attempts"""
    for attempt in range(max_attempts):
        try:
            return action_func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Attempt {attempt+1} failed, retrying: {e}")
            time.sleep(1)
            
def load_page(driver, wait, url):
    """Load page on current window and create wait until the page is fully loaded"""
    driver.get(url)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

def find_search_box(driver, wait):
    """Find the search box in driver"""
    wait.until(EC.presence_of_element_located((By.ID, "sbi_b")))
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    driver.execute_script("arguments[0].focus();", search_box)
                    
    return search_box

def get_points(driver, wait):
    """Get current points from REWARD_URL"""
    try:
        if driver.current_url != REWARD_URL:
            try_with_retry(lambda: load_page(driver, wait, REWARD_URL))
        
        points_element = driver.find_element(By.CSS_SELECTOR, "#balanceToolTipDiv .pointsValue span")
        points_text = points_element.text.strip()
        points = int(points_text.replace(",", ""))
        
        return points

    except Exception as e:
        print(f"Error retrieving points: {e}")
        return -1  
