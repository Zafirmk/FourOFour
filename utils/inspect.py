import json
import time

from .web import scroll

def log_filter(log_):
    return (
        log_["method"] == "Network.responseReceived"
        and "url" in list(log_["params"]["response"].keys())
    )

def inspect(driver, website):

    urls = []

    driver.get(str(website))
    time.sleep(4)
    
    for i in range(3):
        driver.save_screenshot("./temp/" + str(i) + ".png")
        scroll(driver, 350*(i+1))

    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    for log in filter(log_filter, logs):
        resp_url = "".join( log["params"]["response"]["url"].split("/")[:3] )
        if len(resp_url) < len("data:image/png;base64,iVBORw0KGgoAAAANSU"):
            urls.append( resp_url )

    urls_filtered = list(dict.fromkeys(urls))
    return "./temp/" + str(0) + ".png", urls_filtered