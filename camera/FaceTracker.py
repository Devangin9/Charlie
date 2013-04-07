'''
Created on 01-Apr-2013

@author: Devangini
'''
#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
import cv2
import cv2.cv as cv
from optparse import OptionParser
import numpy as np

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING
HCDIR = "E:\\Softwares\\opencv\\data\\haarcascades\\" 
LBPDIR = "E:\\Softwares\\opencv\\data\\lbpcascades\\"


def detect_and_draw(img, cascade, cascade2, cascade3):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        #detect faces
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt11 = (int(x * image_scale) + 10, int(y * image_scale) + 10)
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                #cv.Rectangle(img, pt1, pt11, cv.RGB(0, 255, 0))
#                 print("faces  :::  pt1: " + str(pt1) + "  pt2: " + str(pt2) + "   \n" )
                
#                 print "point 1 " + str(pt1)
                #get the center of the rectangle
                centerX = (pt1[0] + pt2[0])/2     
                centerY = (pt1[1] + pt2[1])/2 + 30
                
                
#                 print "centerX    " + str(centerX)
#                 print "centerY    " + str(centerY)
                
                cv.Rectangle(img, (centerX, centerY), (centerX + 10, centerY + 10), cv.RGB(255, 0, 255))
                
                
                
                
                #detect right eye
                rightEyeArea = cv.GetSubRect(img, (centerX, pt1[1],  pt2[0] - centerX  , centerY - pt1[1]))
                #cv.SetZero(rightEyeArea)    
                rightEye = cv.HaarDetectObjects(rightEyeArea, cascade2, cv.CreateMemStorage(0),
                                             haar_scale, min_neighbors, haar_flags, min_size)
                if rightEye:
                    for ((x, y, w, h), n) in rightEye:
                        # the input to cv.HaarDetectObjects was resized, so scale the
                        # bounding box of each face and convert it to two CvPoints
                        pt3 = (x, y)
                        pt4 = (x + w, y + h)
#                         pt3 = (int(x * image_scale), int(y * image_scale))
#                         pt4 = (int((x + w) * image_scale), int((y + h) * image_scale))
#                         print "point 3 " + str(pt3)
#                         print "point 4 " + str(pt4)
#                         
#                         cv.Rectangle(img, (centerX + pt3[0], pt1[1] + pt3[1]),(centerX + pt4[0], pt1[1] + pt4[1]), cv.RGB(0, 255, 255))
#                         cv.Rectangle(img, pt3, pt4, cv.RGB(0, 0, 255))
                        
                        cv.Rectangle(img, (centerX + pt3[0], pt1[1] + pt3[1]),(centerX + pt4[0], pt1[1] + pt4[1]), cv.RGB(0, 255, 255))
                        #cv.Rectangle(img, pt3, pt4, cv.RGB(0, 0, 255))
                        
#                         print("eyes - right ::::  pt1: " + str(pt1) + "  pt2: " + str(pt2) + "   \n" )
                
                
                
                #detect left eye
                leftEyeArea = cv.GetSubRect(img, (pt1[0], pt1[1], centerX - pt1[0], centerY - pt1[1]))
                #cv.SetZero(sub)  55
                
                leftEye= cv.HaarDetectObjects(leftEyeArea, cascade2, cv.CreateMemStorage(0),
                                             haar_scale, min_neighbors, haar_flags, min_size)
                if leftEye:
                    for ((x, y, w, h), n) in leftEye:
                        # the input to cv.HaarDetectObjects was resized, so scale the
                        # bounding box of each face and convert it to two CvPoints
                        pt3 = (x, y)
                        pt4 = (x + w,y + h)
                        cv.Rectangle(img, (pt1[0] + pt3[0], pt1[1] + pt3[1]),(pt1[0] + pt4[0], pt1[1] + pt4[1]), cv.RGB(255, 255, 0))   
                        
                        
                
                #detect left eyebrow
                #by doing simple contour detection
                gray_im = cv.CreateImage((leftEyeArea.rows, leftEyeArea.cols), 8, 1)
                cv.CvtColor(leftEyeArea, gray_im, cv.CV_RGB2GRAY)
                #floatMat.convertTo(ucharMat, CV_8UC1);

                # scale values from 0..1 to 0..255
                #floatMat.convertTo(ucharMatScaled, CV_8UC1, 255, 0); 
                contours0, hier = cv2.findContours( gray_im , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
              
                print " length " + len(contours0)                
                    
                
                #detect mouth
                mouthArea = cv.GetSubRect(img, (pt1[0],centerY, pt2[0] - pt1[0], pt2[1] - centerY))
                mouth = cv.HaarDetectObjects(mouthArea, cascade3, cv.CreateMemStorage(0),
                                             haar_scale, min_neighbors, haar_flags, min_size)
                if mouth:
                    for ((x, y, w, h), n) in mouth:
                        # the input to cv.HaarDetectObjects was resized, so scale the
                        # bounding box of each face and convert it to two CvPoints
                        pt3 = (x, y)
                        pt4 = (x + w,y + h)    
                        cv.Rectangle(img, (pt1[0] + pt3[0], centerY + pt3[1]),(pt1[0] + pt4[0], centerY + pt4[1]), cv.RGB(255, 255, 255))
                             
                
  
    cv.ShowImage("result", img)

if __name__ == '__main__':

    parser = OptionParser(usage = "usage: %prog [options] [filename|camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = HCDIR + "haarcascade_frontalface_alt_tree.xml")
    
    #parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "../data/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()

    cascade = cv.Load(options.cascade)
     #detect eyes
    cascade2 = cv.Load(HCDIR + "haarcascade_eye_tree_eyeglasses.xml")
    cascade3 = cv.Load(HCDIR + "haarcascade_mcs_mouth.xml")
               

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    input_name = args[0]
    if input_name.isdigit():
        capture = cv.CreateCameraCapture(int(input_name))
    else:
        capture = None

    cv.NamedWindow("result", 1)

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)

            detect_and_draw(frame_copy, cascade, cascade2, cascade3)

            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        detect_and_draw(image, cascade)
        cv.WaitKey(0)

    cv.DestroyWindow("result")

