import pytextnow as pytn
import requests, json
import time
import math
import Credentials
username = Credentials.username()
sid = Credentials.sid()
csrf = Credentials.csrf()
client = pytn.Client(username, sid_cookie=sid, csrf_cookie=csrf)
def weathercheck(msg):
    resp = ""
    city_name = "chicago"
    api_key = Credentials.WeatherKey()
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    timeout = time.perf_counter()
    exitloop = 0
    time.sleep(1)
    msg.send_sms("Please enter city:")
    new_messages = client.get_unread_messages()
    checkagainst = ""
    for message in new_messages:
        message.mark_as_read()
        checkagainst = message.content
    while time.perf_counter() - timeout <= 60 and exitloop != 1:
        time.sleep(1)
        new_messages = client.get_unread_messages()
        exitloop = 0
        for message in new_messages:
            message.mark_as_read()
            resp = message.content #left off working here
        if resp !=  checkagainst:
            exitloop = 1
            city_name = resp
        else:
            exitloop = 0
            city_name = "chicago"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    print(complete_url)
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404" and x["cod"] != "400":
        y = x["main"]
        current_temperature = (y["temp"]*1.8 - 459.67)
        current_temperature = math.floor(current_temperature)
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"] 
        msg.send_sms("weather in " + str(city_name) + ":")
        time.sleep(1)
        msg.send_sms(str(weather_description))
        time.sleep(1)
        msg.send_sms("Temperature: " + str(current_temperature) + "F")
        msg.send_sms("Air Pressure: " + str(current_pressure) +"hpa")
        msg.send_sms("Humidity: " + str(current_humidity) + "%")
    else:
        error1 = "invalid city. please send Weather command again to retry."
        msg.send_sms(error1)
