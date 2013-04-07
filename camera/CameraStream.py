'''
Created on 07-Apr-2013

@author: Devangini
'''
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import numpy as np
#from camera import FaceRec 
from samples.FaceRec import FaceRec




# http://stackoverflow.com/questions/15460706/opencv-cv2-in-python-videocapture-not-releasing-camera-after-deletion
class CameraStream(): 
    
    #
    
         
    def __init__(self,cam,root,canvas):
        self.cam = cam
        self.root = root
        self.canvas = canvas
        self.recognize = FaceRec()
        self.a = None
        self.b = None

    def update_video(self):
        (self.readsuccessful,self.f) = self.cam.read()
        self.gray_im = cv2.cvtColor(self.f, cv2.COLOR_RGB2BGRA)
        #self.gray_im = cv2.cvtColor(self.f, cv2.COLOR_RGB2GRAY)
        self.a = Image.fromarray(self.gray_im)
        self.b = ImageTk.PhotoImage(image=self.a)
        self.canvas.create_image(0,0,image=self.b,anchor=tk.NW)
        self.root.update()
        self.root.after(10,self.update_video)
        
    def trainRecognition(self):
        self.recognize.prepareLearning()
        
        
    def recognisePerson(self):
        self.recognize.identifyPerson(np.asarray(self.a, dtype=np.uint8))
        
        #self.recognize.identifyPerson(self.a)
        #self.recognize.identifyPerson(np.asarray(self.a).astype(np.uint8))
        #self.recognize.identifyPerson(self.a)
       
if __name__ == '__main__':
    root = tk.Tk()
    videoframe = tk.LabelFrame(root,text='Captured video')
    videoframe.grid(column=0,row=0,columnspan=1,rowspan=1,padx=5, pady=5, ipadx=5, ipady=5)
    canvas = tk.Canvas(videoframe, width=480,height=640)
    canvas.grid(column=0,row=0)
    cam = cv2.VideoCapture(2) #2)
    cameraStream = CameraStream(cam,root,canvas)
    cameraStream.trainRecognition()
    root.after(0,cameraStream.update_video)
    labelName = tk.Label(videoframe, text="Hello, world!")
    labelName.grid(column = 0, row = 3)
    buttonQuit = tk.Button(text='Quit',master=videoframe,command=root.destroy)
    buttonShoot = tk.Button(text='Recognize',master=videoframe,command=cameraStream.recognisePerson)
    buttonQuit.grid(column=0,row=1)
    buttonShoot.grid(column=0, row=2)
    root.mainloop()
    del cam