import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def try_with_retry(action_func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return action_func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Attempt {attempt+1} failed, retrying: {e}")
            time.sleep(1)
            
def load_page(driver, wait, url):
    driver.get(url)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

def find_search_box(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "sbi_b")))
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    driver.execute_script("arguments[0].focus();", search_box)
                    
    return search_box