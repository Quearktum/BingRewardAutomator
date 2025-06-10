from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import random
import time
import math
from datetime import datetime, timedelta

from helper import try_with_retry, load_page, find_search_box, get_points
from config import TIMEOUT, WAIT_TIME, REWARD_URL


def reward_search(search_queries, driver):
    completed_searches = 0

    try:
        for search_query in search_queries:
            try:
                wait = WebDriverWait(driver, TIMEOUT)

                execute_search(driver, wait, search_query)
                completed_searches += 1

            except Exception as e:
                print(f"Error during search '{search_query}': {e}")
                continue

        print(f"Completed {completed_searches} out of {len(search_queries)} searches.")
        return completed_searches

    except Exception as e:
        print(f"Fatal error: {e}")
        return completed_searches


def reward_search_interval(search_queries, driver):
    wait = WebDriverWait(driver, TIMEOUT)
    completed_searches = 0
    max_per_interval = 3  # Initial guess for max searches per interval

    # Track points and timing
    last_points = 0
    next_interval_time = datetime.now()
    interval_duration = timedelta(minutes=60)

    print(
        f"Starting interval-optimized search (initial guess: {max_per_interval} searches per {interval_duration})"
    )

    try:
        last_points = get_points(driver, wait)
        print(f"Start iterations with {last_points} points")

        search_index = 0
        while search_index < len(search_queries):
            search_remaining = min(max_per_interval, len(search_queries) - search_index)

            print(f"\n--- New interval at {datetime.now().strftime('%H:%M:%S')} ---")
            print(f"Performing {search_remaining} searches in this interval")

            interval_completed = 0
            for i in range(search_remaining):
                if search_index >= len(search_queries):
                    break

                search_query = search_queries[search_index]
                try:
                    execute_search(
                        driver,
                        wait,
                        search_query,
                    )
                    interval_completed += 1
                    search_index += 1

                    # Add small random delay between searches in same interval
                    if i < search_remaining - 1:
                        delay = random.uniform(300, 600)
                        print(f"Waiting {delay:.1f} seconds before next search...")
                        time.sleep(delay)

                except Exception as e:
                    print(f"Error during search '{search_query}': {e}")
                    search_index += 1
                    continue

            points_gained = get_points(driver, wait) - last_points

            print(f"Gained: {points_gained})")

            if points_gained > 0:
                print(
                    f"✔️ Confirmed: {interval_completed} searches earned points in this interval"
                )

                if interval_completed < max_per_interval:
                    max_per_interval = interval_completed
                    print(f"Update estimate: {max_per_interval} searches per interval")

                last_points = last_points + points_gained
                completed_searches += interval_completed
            else:
                print(
                    f"❌ No points gained in this interval. Testing cooldown period..."
                )

                cooldown_test_intervals = [15, 30, 45, 60, 75, 90]
                for test_minutes in cooldown_test_intervals:
                    print(f"Testing {test_minutes} minute cooldown...")
                    time.sleep(test_minutes * 60)

                    # Try a single search
                    if search_index < len(search_queries):
                        test_query = search_queries[search_index]
                        execute_search(driver, wait, test_query)
                        search_index += 1

                        # Check if point increased
                        test_points = get_points(driver, wait)

                        if test_points > current_points:
                            interval_duration = timedelta(minutes=test_minutes)
                            print(f"✔️ Found cooldown interval: {test_minutes} minutes")
                            last_points = test_points
                            completed_searches += 1
                            break
                        else:
                            current_points = test_points
                            print(f"❌ Still no points after {test_minutes} minutes")

            next_interval_time = datetime.now() + interval_duration
            print(f"Next interval starts at {next_interval_time.strftime('%H:%M:%S')}")

            # Wait until the next interval
            wait_seconds = (next_interval_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"Waiting {wait_seconds/60:.1f} minutes until next interval...")
                time.sleep(wait_seconds)

        print(f"\nCompleted {completed_searches} out of {len(search_queries)} searches")
        print(f"Final estimate: {max_per_interval} searches per {interval_duration}")
        return completed_searches

    except Exception as e:
        print(f"{e}")
        return


def execute_search(driver, wait, search_query):
    """Execute search, wait for WAIT_TIME then close the tab"""
    # Open new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    try_with_retry(lambda: load_page(driver, wait, "https://www.bing.com/"))

    search_box = try_with_retry(lambda: find_search_box(driver, wait))

    # Perform search
    search_box.clear()

    # Human typer
    for char in search_query:
        search_box.send_keys(char)
        time.sleep(0.05)

    # search_box.send_keys(search_query)
    time.sleep(0.2)
    search_box.send_keys(Keys.ENTER)

    time.sleep(WAIT_TIME)

    # Close tab and return to main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
