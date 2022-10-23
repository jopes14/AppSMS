import pytextnow as pytn
import requests, json
import time
import math
import CommWeather
import Credentials
username = Credentials.username()
sid = Credentials.sid()
csrf = Credentials.csrf()
client = pytn.Client(username, sid_cookie=sid, csrf_cookie=csrf)
@client.on("message")
def handler(msg):
    print(msg)
    if msg.type == pytn.MESSAGE_TYPE:
        print(msg.content)
        messagecontent = msg.content
        if str(messagecontent[0]) == "!":
            if messagecontent == "!weather" or messagecontent == "!Weather":
                CommWeather.weathercheck(msg)
            else:
                msg.send_sms("unknown command, please check spelling. Contact Jopes#6969 on discord if you think this is an error")
print("weather sucsessfully returned to user")
