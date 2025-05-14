from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import math

from helper import try_with_retry, load_page
from config import TIMEOUT, WAIT_TIME

           
    
def find_search_box(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "sbi_b")))
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    driver.execute_script("arguments[0].focus();", search_box)
                    
    return search_box

def reward_search(search_queries, driver):
    completed_searches = 0
    
    try:
        for search_query in search_queries:
            try:
                wait = WebDriverWait(driver, TIMEOUT)
                
                # Open new tab
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                            
                try_with_retry(lambda: load_page(driver, wait, "https://www.bing.com/"))
                             
                search_box = try_with_retry(lambda: find_search_box(driver, wait))
                
                # Perform search
                search_box.clear()
                
                # # Human typer
                # for char in search_query:
                #     search_box.send_keys(char)
                #     time.sleep(0.05)  
                
                search_box.send_keys(search_query)
                time.sleep(0.2) 
                search_box.send_keys(Keys.ENTER)
                
                print(f"Performed search {completed_searches+1}: {search_query}")
                
                time.sleep(WAIT_TIME)
                
                # Close tab and return to main tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
                completed_searches += 1
                
            except Exception as e:
                print(f"Error during search '{search_query}': {e}")
                continue  
        
        print(f"Completed {completed_searches} out of {len(search_queries)} searches.")
        return completed_searches
        
    except Exception as e:
        print(f"Fatal error: {e}")
        return completed_searches