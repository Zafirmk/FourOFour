import time
from .web import scroll

def google(driver, search):
    driver.get("https://www.google.com/search?q=" + search)
    time.sleep(1)
    for i in range(3):
        driver.save_screenshot("./temp/" + str(i) + ".png")
        scroll(driver, 350*(i+1))
    return "./temp/0.png"