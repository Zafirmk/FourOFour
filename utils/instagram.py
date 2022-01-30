import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def instagram(driver, username, password):
    _ = get_screenshots(driver, username, password)
    return "./temp/0.png"

def login(driver, username_input, password_input):

    driver.set_window_size(375, 900)

    driver.get("http://www.instagram.com")

    time.sleep(1)

    #target username
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    #enter username and password
    username.clear()
    username.send_keys(username_input)
    password.clear()
    password.send_keys(password_input)

    #target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()


    time.sleep(1.5)
    

def get_elements(driver):
    elements = driver.find_elements_by_xpath("//article[@class='_8Rm4L bLWKA M9sTE _1gNme h0YNM  SgTZ1    ']")
    return elements

def get_screenshots(driver, username, password):
    login(driver, username, password)
    time.sleep(1)
    elements = get_elements(driver)
    for i,elem in enumerate(elements):
        driver.execute_script("return arguments[0].scrollIntoView(false);", elem)
        driver.save_screenshot("./temp/" + str(i) + ".png")
    return elements

def like_image(driver, num):
    elements = get_elements(driver)
    img_to_like = elements[num]
    button_to_press = img_to_like.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[3]/div/article["+str(num+1)+"]/div/div[3]/div/div/section[1]/span[1]/button")
    driver.execute_script("arguments[0].click();", button_to_press)
