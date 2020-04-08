import qwikidata
import random

import speech_recognition as sr
r = sr.Recognizer()

import pyttsx3
engine = pyttsx3.init()
voice_index = random.choice([0,7,10,11,17])
voice=engine.getProperty('voices')[voice_index].id
engine.setProperty('voice',voice)

import templates

with sr.Microphone() as source:
    print('Calibrating...')
    r.adjust_for_ambient_noise(source)
    r.energy_threshold = 150

    #TODO: (Optional) Replace the line below with a 
    #                 conversation opener of your choice
    text = 'Ready with voice %d' % voice_index
    print(text)
    engine.say(text)
    engine.runAndWait()
    while(1):
        #audio = r.listen(source)
        audio = r.record(source,duration = 6)
        try:
            #text = r.recognize_google(audio)
            text = input("text:")
            response = templates.response(text)
        except:
            response = templates.fallback_response()
        print(response)
        engine.say(response)
        engine.runAndWait()
