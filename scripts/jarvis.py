import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia 
import smtplib
import webbrowser as wb
import psutil
import pyautogui
import os
import random
import wolframalpha
import json
import requests
from urllib.request import urlopen

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("The current date is {}, month is {} and, year is {}".format(date, month, year))

def wishme():
    hour = datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
    elif hour>=18 and hour<24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night sir!")
    
    speak("jarvis at your service. Please tell me how can I help you today.    ")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login("sksumi@gmail.com", 'password') # set low security enable in your gmail
    server.sendmail('usermail@gmail.com', to, content)


def cpu_():
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)

    battery = psutil.sensors_battery()
    speak("Battery is {}".format(battery))

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:/Users/sk205/Pictures/Screenshots/screenshot.png")


if __name__ == '__main__':
    # wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query:
            time_()

        elif 'date' in query:
            date_()
        
        elif 'wikipedia' in query:
            query = query.replace("on wikipedia", "")
            speak("Searching {} on wikipedia ...".format(query))
            result = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia {}".format(result))
        
        elif 'send email' in query:
            try:
                speak("What should say?")
                content = TakeCommand()

                # speak = ("Who is the reciever")
                # reciever = input("Enter Email Here--")
                reciever = 'reciever_is_me@gmail.com'
                to = reciever
                sendEmail(to, content)
                speak(content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Unable to send the email.")

        elif 'search on chrome' in query:
            speak("What should I search?")
            search_query = TakeCommand().lower()
            chrome_base_link = "https://www.google.com/search?q=" + search_query
            wb.open(chrome_base_link)

        elif 'search on youtube' in query:
            speak("What should I search?")
            search_query = TakeCommand().lower()
            youtube_base_link = "https://www.youtube.com/results?search_query=" + search_query
            wb.open(youtube_base_link)

        elif 'cpu' in query:
            cpu_() 

        elif 'write a note' in query:
            speak("What should I write, Sir?")
            notes = TakeCommand()
            file = open('notes.txt', 'w')
            speak("Sir should i Include Date and time in it")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(":-")
                file.write(notes)
                speak("Done Taking notes, SIR!")
            else:
                file.write(notes)

        elif 'show notes' in query:
            speak("Showing notes...")
            file = open('notes.txt', 'r')
            print(file.read())
            print(file.read())
        
        elif 'screenshot' in query:
            screenshot()

        elif 'remember that' in query:
            speak("What should I remember?")
            memory = TakeCommand()
            speak("You asked to remember that"+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()
        
        elif 'do you remember anything' in query:
            remember = open('memory.txt', 'r')
            speak('You asked me to remember that'+str(remember.read()))


        elif "weather" in query: 
			
			# Google Open weather website 
			# to get API of Open weather
            api_key = "open weather api"
            base_url = "http://api.openweathermap.org/data /2.5/weather?q="
            speak(" City name ")
            print("City name : ")
            city_name = TakeCommand()
            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
            response = requests.get(complete_url)
            x = response.json()
            
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
                
            else:
                speak(" City Not Found ")
            
        elif 'news' in query:
            
            try:
                speak("Which domain do u interested to hear up about...")
                search_query = TakeCommand().lower()
                api_link = "http://newsapi.org/v2/everything?q={q}&from=2020-12-11&sortBy=publishedAt&apiKey=676edca285ac44c5b3f6e199d36f0355"
                api_link = api_link.format(q=search_query).replace(' ', '-')
                jsonObj = urlopen(api_link)
                
                data = json.load(jsonObj)
                i = 1
                
                speak('here are some top news from the times of india')
                print('''=============== TOP HEADLINES ============'''+ '\n')
                
                for item in data['articles']:
                    
                    print(str(i) + '. ' + item['title'] + '\n') 
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
                    
            except Exception as e:
                print(str(e))
        
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            wb.open("https://www.google.com/maps/place/" + location + "")

        # most asked question from google Assistant
        elif "will you be my gf" in query or "will you be my bf" in query:
            speak("I'm not sure about, may be you should give me some time")
            
        elif "i love you" in query:
            speak("It's hard to understand, I am still trying to figure this out.")

        elif "calculate" in query:
            
            app_id = "T722VX-RT9T6KAWJ3"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)


        elif "what is" in query or "who is" in query: 
            client = wolframalpha.Client("T722VX-RT9T6KAWJ3")
            res = client.query(query)
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results") 

        
        elif 'tell me' in query:

            client = wolframalpha.Client("T722VX-RT9T6KAWJ3")
            query = query.replace('tell me', '')
            res = client.query(query)

            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results")
        
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much seconds you want me to stop listening commands")
            a = int(TakeCommand())
            time.sleep(a)
            print(a)

        elif 'go offline' in query:
            speak("Going offline sir!")
            quit()
        
        elif 'log out' in query:
            os.system("shutdown -l")

        elif "restart the system" in query or "restart system" in query:
            os.system("shutdown /r /t l")
        
        elif 'shutdown' in query:
            os.system("shutdown /s /t l")

