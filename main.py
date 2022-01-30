# Server Imports
import os
import requests
from flask import Flask, request
from flask import send_from_directory

# SMS/MMS Imports
from twilio.twiml.messaging_response import MessagingResponse

# Headless Browsing Imports
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

# Custom utils
import pickle
import validators
from utils.inspect import inspect
from utils.web import website
from utils.google import google
from utils.instagram import instagram

app = Flask(__name__)

database_simulator = {}

db = './temp/database_simulator.pkl'
with open(db, 'wb') as f:
    pickle.dump(database_simulator, f)

tmp_folder = "./temp"
tmp_file = tmp_folder + '/temp.png'

ngrok_url = 'https://aea6-184-162-252-127.ngrok.io'  # REPLACE THIS WITH YOUR FORWARDING URK
upload_path = ngrok_url + "/uploads"

tmp_file_path = upload_path + "/temp.png"

def get_driver():
    option = webdriver.ChromeOptions()

    option.add_argument("window-size=1280,800")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"} 

    driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities, options=option)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.implicitly_wait(30) # drop if unable to login
    # driver.set_window_size(375, 900)

    return driver

@app.route('/entry', methods=['POST'])
def entry():

    incoming_text = request.values.get('Body', '').split(" ")

    if len(incoming_text) > 2:
        incoming_text[0] = incoming_text[0].lower()
        incoming_text[1] = incoming_text[1].lower()
    else:
        for i, j in enumerate(incoming_text):
            incoming_text[i] = j.lower()

    with open(db, 'rb') as f:
        database_simulator = pickle.load(f)

    if incoming_text[0] == "instagram":

        driver = get_driver()

        if len(incoming_text) < 3 or len(incoming_text) > 3:
            resp = MessagingResponse()
            msg = resp.message()
            msg.body( "Did'nt understand request! \nTo check 'instagram' followed by username and password (space seperated) ")
            driver.quit()
            return str(resp)

        for i in range(3):
            file_ = tmp_folder + "/" + str(i) + ".png"
            if os.path.isfile(file_):
                os.remove(file_)

        media_loc = instagram(driver, incoming_text[1], incoming_text[2])

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        resp = MessagingResponse()
        msg = resp.message()
        msg.media(tmp_file_path)

        driver.quit()
        return str(resp)


    elif incoming_text[0] == "google":

        driver = get_driver()

        search_req = "+".join(incoming_text[1:])

        media_loc = google(driver, search_req)

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        resp = MessagingResponse()
        msg = resp.message()
        msg.media(tmp_file_path)

        driver.quit()
        return str(resp)

    elif incoming_text[0] == "inspect":

        driver = get_driver()

        media_loc, results = inspect(driver, incoming_text[1])
        print("Length ", len(results))

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        body = "Requests Made\n"

        body += "\n".join( results )

        resp = MessagingResponse()
        msg = resp.message()

        msg.body(body)

        driver.quit()
        return str(resp)

    elif incoming_text[0] == "set":

        
        if len(incoming_text) < 3 or len(incoming_text) > 3:
            resp = MessagingResponse()
            msg = resp.message()
            msg.body( "Did'nt understand request! \nTo save a link send  'set' followed by the name you want to set as and the URL")
            return  str(resp)

        database_simulator[ incoming_text[1] ] = incoming_text[2]
        with open(db, 'wb') as f:
            pickle.dump(database_simulator, f)

        resp = MessagingResponse()
        msg = resp.message()
        msg.body( "Website: " + incoming_text[2] + " - saved as " + incoming_text[1] )
        return str(resp)

    elif incoming_text[0] in list(database_simulator.keys()):
        
        driver = get_driver()

        if not validators.url( str( database_simulator[ incoming_text[0] ]) ):
            resp = MessagingResponse()
            msg = resp.message()
            msg.body( "An error occured - " +  database_simulator[ incoming_text[0] ])
            return str(resp)

        media_loc = website(driver, database_simulator[ incoming_text[0] ])

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        resp = MessagingResponse()
        msg = resp.message()
        msg.media(tmp_file_path)

        driver.quit()
        return str(resp)

    elif incoming_text[0] == "scroll":

        for i in range(3):
            f = "./temp/" + str(i) + ".png"
            if os.path.isfile(f):

                if os.path.isfile(tmp_file):
                    os.remove(tmp_file)
                    
                os.rename(f, tmp_file)

                resp = MessagingResponse()
                msg = resp.message()
                msg.media(tmp_file_path)

                return str(resp)

    elif "." in incoming_text[0]:

        driver = get_driver()

        media_loc = website(driver, "https://" + incoming_text[0])

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        resp = MessagingResponse()
        msg = resp.message('Loaded')
        msg.media(tmp_file_path)

        driver.quit()
        return str(resp)

    else:

        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Invalid command!")
        return str(resp)

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(tmp_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4545)