'''
Created on 05-Apr-2013

@author: Devangini
'''

#https://code.google.com/p/computervision/source/browse/trunk/displayImageTkinter.py?r=9

#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Philipp Wagner <bytefish[at]gmx[dot]de>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the author nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.




import os
import sys
import cv2
import numpy as np
from camera import Camera

from Tkinter import *
import Tkinter as tk #the windowing and event system. 

import cv2.cv as cv

#from opencv.highgui import *        #being used for capturing images and not display
#from opencv.adaptors import *      #converting to PIL 
#from PIL import  ImageTk               #converting to tkinter 



class FaceRec:

    model = None
    peopleNames = []

    def normalize(self, X, low, high, dtype=None):
        """Normalizes a given array in X to a value between low and high."""
        X = np.asarray(X)
        minX, maxX = np.min(X), np.max(X)
        # normalize to [0...1].
        X = X - float(minX)
        X = X / float((maxX - minX))
        # scale to [low...high].
        X = X * (high - low)
        X = X + low
        if dtype is None:
            return np.asarray(X)
        return np.asarray(X, dtype=dtype)


    def callback(self):
        print "called the callback!"
        
    def identifyPerson(self, imageName):
        #im = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
    #                   
        #matrix  = cv2.cvtColor(imageName, cv2.COLOR_GRAY2BGR)
        matrix = cv.fromarray(imageName)
        
        #newImage = cv.CreateMat(480, 640, cv.CV_32FC1)
        newImage = cv.CreateMat(480, 640, cv.CV_8UC1)
        #print matrix.type()
        #cv.Resize(np.asarray(imageName), newImage)
        
        cv.Convert(matrix, newImage)
        imageName = np.asarray(newImage)
        #print imageName 
        output = self.model.predict(imageName)
        #print output
        [p_label, p_confidence] = output
        # Print it:
        print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)
        return self.peopleNames[p_label]
    
    def read_images(self, path, sz=None):
        """Reads the images in a given folder, resizes images on the fly if size is given.
    
        Args:
            path: Path to a folder with subfolders representing the subjects (persons).
            sz: A tuple with the size Resizes
    
        Returns:
            A list [X,y]
    
                X: The images, which is a Python list of numpy arrays.
                y: The corresponding labels (the unique number of the subject, person) in a Python list.
        """
        c = 0
        X = []
        y = []
        for dirname, dirnames, filenames in os.walk(path):
    #         print dirname
    #         print dirnames
    #         print filenames
            for subdirname in dirnames:
                self.peopleNames.append(subdirname)
    #             print subdirname
                subject_path = os.path.join(dirname, subdirname)
    #             print subject_path
                for filename in os.listdir(subject_path):
    #                 print filename
                    try:
                        image_name = os.path.join(subject_path, filename)
    #                     print image_name
                        im = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
                       
    #                     print im
                        # resize to given size (if given)
                        if (sz is not None):
                            im = cv2.resize(im, sz)
                        # print im
                        image = np.asarray(im, dtype=np.uint8)
                        
                        # to knpw the dimensions of the image
                        #mat = cv.fromarray(im)
                        # mat.rows
                        #print mat.cols
                        X.append(image)
                        y.append(c)
                        
                        
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                c = c + 1
        return [X, y]
    
   
        
    def prepareLearning(self):
        # This is where we write the images, if an output_dir is given
        # in command line:
        out_dir = None
        # You'll need at least a path to your image data, please see
        # the tutorial coming with this source code on how to prepare
        # your image data:
        # if len(sys.argv) < 2:
            # print "USAGE: facerec_demo.py </path/to/images> [</path/to/store/images/at>]"
            # sys.exit()
        # Now read in the image data. This must be a valid path!
        [X, y] = self.read_images("E:\\python workspace\\Charlie\\people")
        # Convert labels to 32bit integers. This is a workaround for 64bit machines,
        # because the labels will truncated else. This will be fixed in code as
        # soon as possible, so Python users don't need to know about this.
        # Thanks to Leo Dirac for reporting:
        y = np.asarray(y, dtype=np.int32)
        # If a out_dir is given, set it:
        # if len(sys.argv) == 3:
         # out_dir = sys.argv[2]
        # Create the Eigenfaces model. We are going to use the default
        # parameters for this simple example, please read the documentation
        # for thresholding:
        self.model = cv2.createEigenFaceRecognizer()
        # Read
        # Learn the model. Remember our function returns Python lists,
        # so we use np.asarray to turn them into NumPy lists to make
        # the OpenCV wrapper happy:
        self.model.train(np.asarray(X), np.asarray(y))
        # We now get a prediction from the model! In reality you
        # should always use unseen images for testing your model.
        # But so many people were confused, when I sliced an image
        # off in the C++ version, so I am just using an image we
        # have trained with.
        #
        # model.predict is going to return the predicted label and
        # the associated confidence:
        print "finisehed training"
     
        
    def drawGui(self):
        
        root = Tk()
        
        # create a menu
        menu = Menu(root)
        root.config(menu=menu)
    
        filemenu = Menu(menu)
        menu.add_cascade(label="Identify", menu=filemenu)
        filemenu.add_command(label="Person", command=self.identifyPerson)
        filemenu.add_command(label="Open...", command=self.callback)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.callback)
    
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.callback)
        
        
        
       
        Label(text="one").pack()
        
        separator = Frame(height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)
        
        Label(text="two").pack()



# OpenCV has a convienient, builtin windowing and file handling system contained in highgui. However, it is reccomended that for serious applications that something else is used, tkinter in this case. Although, highgui is still being used for the capturing of images form the camera. OpenCV also has an adaptors module, for converting images between it and, openCV formats and NumPy or PIL. Most importantly, openCV contains the cv module which contains the computer vision algorithms.
# 
# 
# 
# FOR HELP
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/521918
# http://effbot.org/tkinterbook/label.htm


#TODO: try the suggestion bellow, with something like var = ImageVar, and we could do without the loop.
#http://effbot.org/tkinterbook/label.htm
#Label(master, textvariable=v).pack()
#You can associate a Tkinter variable with a label. When the contents of the variable changes, the label is automatically updated:
#v = StringVar()
#v.set("New Text!")

#TODO:put in a delay so that we are not waisting resource
#TODO:add a lable holder to avoid blank images
#TODO:kill window correctly, including cleanly exiting the web cam.
#TODO:

        cam=cv2.VideoCapture(0)
        
        #img = cv.QueryFrame(cam)
        #cv.ShowImage("camera", img)
        cam.release

    
        mainloop()
        
        # Cool! Finally we'll plot the Eigenfaces, because that's
        # what most people read in the papers are keen to see.
        #
        # Just like in C++ you have access to all model internal
        # data, because the cv::FaceRecognizer is a cv::Algorithm.
        #
        # You can see the available parameters with getParams():
    #     print model.getParams()
        # Now let's get some data:
    #     mean = model.getMat("mean")
    #     eigenvectors = model.getMat("eigenvectors")
    #     # We'll save the mean, by first normalizing it:
    #     mean_norm = normalize(mean, 0, 255, dtype=np.uint8)
    #     mean_resized = mean_norm.reshape(X[0].shape)
    #     if out_dir is None:
    #         cv2.imshow("mean", mean_resized)
    #     else:
    #         cv2.imwrite("%s/mean.png" % (out_dir), mean_resized)
    #     # Turn the first (at most) 16 eigenvectors into grayscale
    #     # images. You could also use cv::normalize here, but sticking
    #     # to NumPy is much easier for now.
    #     # Note: eigenvectors are stored by column:
    #     for i in xrange(min(len(X), 16)):
    #         eigenvector_i = eigenvectors[:,i].reshape(X[0].shape)
    #         eigenvector_i_norm = normalize(eigenvector_i, 0, 255, dtype=np.uint8)
    #         # Show or save the images:
    #         if out_dir is None:
    #             cv2.imshow("%s/eigenface_%d" % (out_dir,i), eigenvector_i_norm)
    #         else:
    #             cv2.imwrite("%s/eigenface_%d.png" % (out_dir,i), eigenvector_i_norm)
    #     # Show the images:
#         if out_dir is None:
#             cv2.waitKey(0)
#     

if __name__ == "__main__":
    rec = FaceRec()
    rec.recogniseFace()
    rec.drawGui()
        