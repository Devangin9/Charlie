'''
Created on 17-Mar-2013

@author: Devangini
'''
import subprocess

def textToWav(text,file_name):
   subprocess.call(["espeak",text,"-w"+file_name+".wav"])

textToWav('hello world','hello')