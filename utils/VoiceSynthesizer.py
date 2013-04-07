'''
Created on 17-Mar-2013

@author: Devangini
'''
import pyttsx
engine = pyttsx.init()

voices = engine.getProperty('voices')
print(voices)
for voice in voices:
   voice.gender = 'male'
   
   voice.gender
   engine.setProperty('voice', voice.id)
#    engine.setProperty('gender', 'male')
   engine.say('My name is Charlie the robot. I love humans.')
engine.runAndWait()


engine.runAndWait()