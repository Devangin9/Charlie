'''
Created on 01-Apr-2013

@author: Devangini

This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
'''
#!/usr/bin/python



import sys
import cv2
import cv2.cv as cv
from optparse import OptionParser
import numpy as np
from samples import hist
import colorsys

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
DATADIR2 = "E:\\Softwares\\opencv\\data\\extracascades\\" 
LBPDIR = "E:\\Softwares\\opencv\\data\\lbpcascades\\"
DATADIR = "E:\\python workspace\\Charlie\\data\\"



hsv_map = np.zeros((180, 256, 3), np.uint8)
h, s = np.indices(hsv_map.shape[:2])
hsv_map[:,:,0] = h
hsv_map[:,:,1] = s
hsv_map[:,:,2] = 255
hsv_map = cv2.cvtColor(hsv_map, cv2.COLOR_HSV2BGR)

hist_scale = 10
def set_scale(val):
    global hist_scale
    hist_scale = val
cv2.createTrackbar('scale', 'hist', hist_scale, 32, set_scale)

def hs_histogram(src):
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    # Extract the H and S planes
    h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
    s_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    h_bins = 180
    s_max  = 255
    s_bins = s_max
    hist_size = [h_bins, s_bins]
    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]
    # saturation varies from 0 (black-gray-white) to
    # 255 (pure spectrum color)
    
    s_ranges = [0, s_max]
    ranges = [h_ranges, s_ranges]
    scale = 10
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)
    cv.NormalizeHist(hist, 1)
    (_, max_value, _,max_idx ) = cv.GetMinMaxHistValue(hist)
    
    print "max value  " + str(max_value)
    print "max value coords " + str(max_idx)
    print "range " + str(colorsys.rgb_to_hsv(1, 1, 1))
    print "color "  + str(colorsys.hls_to_rgb(14/180,1,  114/255))
    print "size " + str(hist_size)

    hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)

    for h in range(h_bins):
        for s in range(s_bins):
            bin_val = cv.QueryHistValue_2D(hist, h, s)
            intensity = cv.Round(bin_val * 255 / max_value)
            cv.Rectangle(hist_img,
                         (h*scale, s*scale),
                         ((h+1)*scale - 1, (s+1)*scale - 1),
                         cv.RGB(intensity, intensity, intensity), 
                         cv.CV_FILLED)
    return hist_img


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
                centerY = (pt1[1] + pt2[1])/2 + int(0.1 * w * image_scale)
                
                
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
#                 print type(leftEyeArea)
#                 gray_im = cv.CreateMat(leftEyeArea.height, leftEyeArea.width, cv.CV_8UC1)
#                 #gray_im = cv.CreateImage((leftEyeArea.rows, leftEyeArea.cols), cv.IPL_DEPTH_8U, 1)
#                 print type(gray_im)
#                 cv.CvtColor(leftEyeArea, gray_im, cv.CV_RGB2GRAY)
#                 imageArray = np.asarray(gray_im, dtype=np.uint8)
#                 #floatMat.convertTo(ucharMat, CV_8UC1);
# 
#                 # scale values from 0..1 to 0..255
#                 #floatMat.convertTo(ucharMatScaled, CV_8UC1, 255, 0); 
#                 contours0, hier = cv2.findContours( imageArray , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#               
#                 print " length " + str(len(contours0))   
#                 print type(contours0)
                
                
                
            
                
                #for item in contours0:
                 #   print "item " + str(item)
                  
                    #print type(item)
                    #for i in range(1, len(item))
                      #  print i
                        
                #for i = 1 : len(contours0)
                
                
                # find good features
#                 eig_image = cv.CreateMat(gray_im.rows, gray_im.cols, cv.CV_32FC1)
#                 temp_image = cv.CreateMat(gray_im.rows, gray_im.cols, cv.CV_32FC1)
#                 for (x,y) in cv.GoodFeaturesToTrack(gray_im, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True):
#                     print "good feature at", x,y
#                     cv.Rectangle(img, (int(x), int(y)),(int(x) + 20, int(y) + 20), cv.RGB(255, 255, 255))
                        
                
                    
                #find color of the skin
                #prepare histogram
                
            
                eyebrow_Area = cv.GetSubRect(img, (pt1[0], int(pt1[1] * 1.1), centerX - pt1[0], int((centerY - pt1[1])*0.6)))
                
                hsv_image = cv.CreateMat(eyebrow_Area.height, eyebrow_Area.width, cv.CV_8UC3)
                imageArray = np.asarray(eyebrow_Area, dtype=np.uint8)
                hsv_image  = cv2.cvtColor(imageArray, cv2.COLOR_BGR2HSV)
                
                
#                 histogram2 = hs_histogram(leftEyeArea)
#                 print(histogram2)
#                 imageArray2 = np.asarray(histogram2, dtype=np.uint8)
#                 cv2.imshow("histo " , histogram2)
                
#                 
                #dark = imageArray[...,2] < 32
                #set not frequent to dark
                #imageArray[dark] = 0
                #histogram = cv.CreateHist(2, cv.CV_HIST_ARRAY)
                histogram = cv2.calcHist( [hsv_image], [0, 1], None, [180, 256], [0, 180, 0, 256] )
                
                
                
                
                
                h1 = np.clip(histogram*0.005*hist_scale, 0, 1)
                vis = hsv_map*h1[:,:,np.newaxis] / 255.0
                #print type(vis)
                cv2.imshow('hist', vis)
                
                
                #backproj = None
                #cv.CalcBackProject(hsv_image, backproj, histogram)
                ranges = [0, 180, 0, 256]
                backproj = cv2.calcBackProject([hsv_image], [0, 1], histogram, ranges, 10)
                cv2.imshow("back proj ", backproj)
                
                #now apply mask for values in range +/- 10% of index_1
                #form a map for showing the eyebrows
                #cloneImageArray = cv.CloneMat(imageArray)
                cloneImageArray = np.empty_like (imageArray)
                cloneImageArray[:] = imageArray
                cv2.imshow("left eye " ,cloneImageArray)
            
                res = cv2.bitwise_and(cloneImageArray,cloneImageArray,mask = backproj)
                cv2.imshow("res" ,res)
            
               
                           
                #find max
#                 minValue = len(vis[0])
#                 index_1 = -1
#                 index_2 = -1
#                 count = 10
#                 for x in range(len(vis)):
#                     for y in range(len(vis[x])):
#                         value = y 
#                         if value < minValue:
#                             minValue = value
#                             index_1 = x
#                             index_2 = y
#                             count = 2
#                 print "max " + str(len(vis[0]) - minValue)  + " " + str(index_1) + " , " + str(index_2)  + " -> " + str(imageArray[index_1][index_2]) + " : " + str(count)      
                
               
                
#                 frequentHueValue = hsv_image[index_1][index_2][0]
#                 
#                 print "freq hue value " + str(frequentHueValue)
#                 
#                 for x in range(len(vis)):
#                     for y in range(len(vis[x])):
#                         #just consider hue value
#                         if abs(hsv_image[x][y][0] - frequentHueValue)/frequentHueValue < 10:
#                             cloneImageArray[x][y][0] = 0
#                             cloneImageArray[x][y][1] = 0
#                             cloneImageArray[x][y][2] = 0
                            
                
                
                
               
                
                
                #projection = cv2.calcBackProject([gray_im], [0,1], histogram, [180, 256], 1.0)
                #projection = None
                #cv.CalcBackProject(leftEyeArea, projection, histogram)
                #cv2.imshow("back proj ", projection)
                
                #find max frequency
                #print type(vis)
                #maxIndex = np.argmax([0, vis])
                #print "maxColor " + str(maxIndex)
                
                #(max, min) = cv.GetMinMaxHistValue(histogram)
                #print "max " + str(max)
                
                # normalize histogram and apply backprojection
                #cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)
                #cv2.imshow("normalized histogram ", histogram)
                
                #find min and max
                #output = cv.GetMinMaxHistValue(histogram)
                #print output
                
                
                
                #dst = cv2.calcBackProject([gray_im],[0,1],histogram,[0,180,0,256],255 / histogram.max())
                 
                #cv2.imshow("back proj ", dst)
                 
                #print len(dst)
                #print "frequent color is " + str(dst[len(dst) - 1])
                # 
                # Now convolute with circular disc
                #disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
                #cv2.filter2D(dst,-1,disc,dst)
                 
                # threshold and binary AND
                #ret,thresh = cv2.threshold(dst,50,255,0)
                #thresh = cv2.merge((thresh,thresh,thresh))
                #res = cv2.bitwise_and(target,thresh)
                 
                #res = np.vstack((target,thresh,res))
                #cv2.imwrite('res.jpg',res)

        
                
                #detect mouth
                mouthArea = cv.GetSubRect(img, (pt1[0],centerY, pt2[0] - pt1[0], pt2[1] - centerY ))
                
                mouth = cv.HaarDetectObjects(mouthArea, cascade3, cv.CreateMemStorage(0),
                                             haar_scale, min_neighbors, haar_flags, min_size)
                if mouth:
                    for ((x, y, w, h), n) in mouth:
                        # the input to cv.HaarDetectObjects was resized, so scale the
                        # bounding box of each face and convert it to two CvPoints
                        pt3 = (x, y)
                        pt4 = (x + w,y + h)    
                        cv.Rectangle(img, (pt1[0] + pt3[0], centerY + pt3[1]),(pt1[0] + pt4[0], centerY + pt4[1]), cv.RGB(0, 0, 255))
                             
                
  
    cv.ShowImage("result", img)

if __name__ == '__main__':

    parser = OptionParser(usage = "usage: %prog [options] [filename|camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = HCDIR + "haarcascade_frontalface_alt_tree.xml")
    
    #parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "../data/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()

    cascade = cv.Load(options.cascade)
     #detect eyes
    cascade2 = cv.Load(DATADIR2 + "haarcascade eye.xml")
    #cascade2 = cv.Load(HCDIR + "..\\eyes\\eye.xml")
   
    #cascade3 = cv.Load(HCDIR + "haarcascade_mcs_mouth.xml")
    cascade3 = cv.Load(DATADIR2 + "Mouth.xml")
               

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

