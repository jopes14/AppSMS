import pytextnow as pytn
import requests, json
import time
import math
#ignore the username please
client = pytn.Client("Text now username", sid_cookie="sid_cookie", csrf_cookie="csrf_cookie") #i removed login information for obvious reasons
Commandslist = ["weather", "Weather"]
@client.on("message") #when a message is sent
def handler(msg):
    print(msg)
    if msg.type == pytn.MESSAGE_TYPE:
        if msg.content == "weather" or "Weather":
            if msg.content == "weather" or "Weather":
                resp = ""
                city_name = "chicago" #defaults city_name to chicago
                api_key = "api_key" # need to put open weather map api key here
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                timeout = time.perf_counter() #checks the program time right before the loop starts
                exitloop = 0
                msg.send_sms("Please enter city:")
                new_messages = client.get_unread_messages()
                checkagainst = ""
                for message in new_messages:
                        message.mark_as_read()
                        checkagainst = message.content # gets the original last message to check against in the loop
                while time.perf_counter() - timeout <= 60 and exitloop != 1: #continually checks to see if there is a new message
                    new_messages = client.get_unread_messages()
                    exitloop = 0
                    for message in new_messages:
                        message.mark_as_read()
                        resp = message.content 
                    if resp !=  checkagainst:
                        exitloop = 1
                        city_name = resp
                    else:
                        exitloop = 0
                        city_name = "chicago" #if nothing is entered within 60 seconds it defaults to chicago
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                print(complete_url)
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = (y["temp"]*1.8 - 459.67) #temp is normally in kelvin
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
                    msg.send_sms("invalid city. please send \"Weather\" command again to retry.") #if the link returns a 404 then invalid city was entered
        else:
            msg.send_sms("unknown command, please check spelling/capitilazation. Contact Jopes#6969 on discord if you think this is an error")
print("weather sucsessfully returned to user")
