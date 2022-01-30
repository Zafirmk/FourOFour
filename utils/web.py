import time

def scroll(driver, amnt="350"):
    driver.execute_script("window.scrollTo(0, " + str(amnt) + ");")

def website(driver, website):
    driver.get(str(website))
    time.sleep(0.5)
    for i in range(3):
        driver.save_screenshot("./temp/" + str(i) + ".png")
        scroll(driver, 350*(i+1))
    return "./temp/" + str(0) + ".png"