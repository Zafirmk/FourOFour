from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from InstagramSeleniumBot import get_screenshots
from InstagramSeleniumBot import like_image

driver = webdriver.Chrome('/Users/zafirkhalid/Desktop/ConUHacks/chromedriver')

def scroll():
    driver.execute_script("window.scrollTo(0, 350);")
    driver.save_screenshot("image_scroll.png")

def website(website,ext=""):
    driver.get("https://www."+str(website)+".com" + str(ext))
    time.sleep(1)
    driver.save_screenshot("image_website.png")

def google(search):
    driver.get("https://www.google.com/?hl=en")
    search_input = driver.find_element_by_name('q')
    search_input.send_keys(search)
    time.sleep(1)
    button_to_press = driver.find_element_by_css_selector('input[type="submit"]')
    button_to_press.click()
    time.sleep(1)
    driver.save_screenshot("image_google.png")

def instagram(driver, username, password):
    get_screenshots(driver, username, password)

def likeimage(driver, imagenum):
    likeimage(driver, imagenum)
