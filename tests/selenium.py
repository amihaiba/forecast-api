# Worksheet   : Testing Methodology
# Author      : Amihai Ben-Arush
# Code review :
# Description : Test unit using selenium to check both positive and negative location results
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
# Downloaded geckodriver and installed in /usr/bin/geckdriver
# Created a symlink for the firefox launcher:
# sudo ln -s /usr/bin/firefox /snap/firefox/current/firefox.launcher


def test_positive():
    """Positive test of the web location search function"""
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get("http://127.0.0.1:5000")

    # Make sure the page was reached and is correct
    title = driver.title
    assert title == "Weather Forecast"
    driver.implicitly_wait(0.5)

    # Get the search field and the search button
    text_box = driver.find_element(by=By.ID, value="text-box")
    submit_button = driver.find_element(by=By.ID, value="button")
    # Input real location and click the search button
    text_box.send_keys("Jerusalem")
    submit_button.click()

    # Check if a location was found
    title = driver.find_element(by=By.CSS_SELECTOR, value="p.display-6").text
    assert title != "Location not found"

    driver.quit()


def test_negative():
    """Negative test of the web location search function"""
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get("http://127.0.0.1:5000")

    # Make sure the page was reached and is correct
    title = driver.title
    assert title == "Weather Forecast"
    driver.implicitly_wait(0.5)

    # Get the search field and the search button
    text_box = driver.find_element(by=By.ID, value="text-box")
    submit_button = driver.find_element(by=By.ID, value="button")
    # Input wrong location and click the search button
    text_box.send_keys("Bamboplompa")
    submit_button.click()
    # Check if a location was not found
    title = driver.find_element(by=By.CSS_SELECTOR, value="p.display-6").text
    assert title == "Location not found"

    driver.quit()


if __name__ == '__main__':
    pass
