# Server Imports
import os
import requests
from flask import Flask, request
from flask import send_from_directory

# SMS/MMS Imports
from twilio.twiml.messaging_response import MessagingResponse

# Headless Browsing Imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Custom utils
from utils.web import website
from utils.google import google
from utils.instagram import instagram

app = Flask(__name__)

database_simulator = {}

tmp_folder = "./temp"
tmp_file = tmp_folder + '/temp.png'

ngrok_url = 'https://5879-184-162-252-127.ngrok.io'
upload_path = ngrok_url + "/uploads"

tmp_file_path = upload_path + "/temp.png"

@app.route('/entry', methods=['POST'])
def entry():

    incoming_text = request.values.get('Body', '').lower().split(" ")

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_text[0] == "instagram":

        option = webdriver.ChromeOptions()
        option.add_argument("window-size=1280,800")
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        if len(incoming_text) < 3 or len(incoming_text) > 3:
            msg.body( "Did'nt understand request! \nTo check 'instagram' followed by username and password (space seperated) ")
            driver.close()
            return str(resp)

        media_loc = instagram(driver, incoming_text[1], incoming_text[2])
        os.rename(media_loc, tmp_file)

        msg.media(tmp_file_path)
        resp = str(resp)

        driver.close()
        return  resp


    elif incoming_text[0] == "google":

        driver = webdriver.Chrome(ChromeDriverManager().install())

        search_req = "+".join(incoming_text[1:])

        media_loc = google(driver, search_req)

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        msg.media(tmp_file_path)
        resp = str(resp)

        driver.close()
        return  resp

    elif incoming_text[0] == "set":

        
        if len(incoming_text) < 3 or len(incoming_text) > 3:
            msg.body( "Did'nt understand request! \nTo save a link send  'set' followed by the name you want to set as and the URL")
            return  str(resp)

        database_simulator[ incoming_text[1] ] = incoming_text[2]
        msg.body( "Website: " + incoming_text[2] + " - saved as " + incoming_text[1] )
        return  str(resp)

    elif incoming_text[0] in list(database_simulator.keys()):
        
        driver = webdriver.Chrome(ChromeDriverManager().install())

        media_loc = website(driver, database_simulator[ incoming_text[0] ])

        if os.path.isfile(tmp_file):
            os.remove(tmp_file)

        os.rename(media_loc, tmp_file)

        msg.media(tmp_file_path)
        resp = str(resp)

        driver.close()
        return  resp

    elif incoming_text[0] == "scroll":

        for i in range(3):
            f = "./temp/" + str(i) + ".png"
            if os.path.isfile(f):

                if os.path.isfile(tmp_file):
                    os.remove(tmp_file)
                    
                os.rename(f, tmp_file)

                msg.media(tmp_file_path)
                resp = str(resp)

                return  resp

    else:

        msg.body("Invalid command!")
        return  str(resp)

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(tmp_folder, filename)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=4545)