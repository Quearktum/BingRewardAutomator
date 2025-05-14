import time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import REWARD_URL, TIMEOUT, WAIT_TIME
from helper import try_with_retry, load_page


def daily_sets(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    
    try:
        try_with_retry(lambda: load_page(driver, wait, REWARD_URL))
        
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ds-card-sec .ng-scope")))
        
        tasks = driver.find_elements(By.CSS_SELECTOR, "#daily-sets .mee-icon-AddMedium")      
        print(f"Found {len(tasks)} card elements")
        
        for task in tasks:
            try:
                task_link = task.find_element(By.XPATH, "./ancestor::a")
                # Open task link
                task_link.click()
                driver.switch_to.window(driver.window_handles[-1])
                
                time.sleep(WAIT_TIME)
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
            except Exception as e:
                print(f"Error processing task: {e}")
        
        return "Daily Tasks completed."
    except Exception as e:
        print(f"Error completing daily sets: {e}")
        return
