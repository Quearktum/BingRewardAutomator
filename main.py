from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import math
from search_query import get_search_query, execute_prompt
from reward_search import reward_search
from num_search_need import num_search_need


search_queries = [] 

if __name__ == "__main__":  
    driver = webdriver.Edge()
    
    search_times = num_search_need(driver)
    
    if (search_times > 0):
        prompt = get_search_query(search_times)
        search_queries = execute_prompt(prompt)
        
        reward_search(search_queries, driver)
    
    print("Job completed, quitting...")
    driver.quit()
