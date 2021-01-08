import requests
import speech_recognition as sr
import pyttsx3 

converter = pyttsx3.init() 
converter.setProperty('rate', 150) 
converter.setProperty('volume', 0.7) 
voices = converter.getProperty('voices')
converter.setProperty('voice', voices[1].id)
  
rec = sr.Recognizer()

bot_message = ""

while(True):
    with sr.Microphone(device_index=0) as source:
        print("Jarvis is Listening...")
        message = rec.listen(source)

    try:
        query = rec.recognize_google(message, language="en-in")
        print("You Said : {}".format(query))
        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message":query})

        for i in r.json():
            print("Jarvis Said : {}".format(i['text']))
            bot_message = i['text']
            converter.say(bot_message)
            converter.runAndWait() 

    except Exception as e:
        converter.say(e)
        converter.runAndWait() 
