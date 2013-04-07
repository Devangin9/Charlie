'''
Created on 01-Apr-2013

@author: Devangini
'''

import cv2.cv as cv



def takePicture(self):
    capture = cv.CaptureFromCAM(0)
    img = cv.QueryFrame(capture)
    # 'string%d' % (i,)
    path = "E:\\python workspace\\Charlie\\images\\person.jpg"
    cv.SaveImage( path , img)
    return path


       
    

def captureFromCamera(self):

    #cv.NamedWindow("camera", 1)
    capture = cv.CaptureFromCAM(0)
    
    
    


    i = 0
    while True:
        img = cv.QueryFrame(capture)
        # 'string%d' % (i,)
        cv.SaveImage("E:\\python workspace\\Charlie\\images\\image%d.jpg" % (i)  , img)
        i=i+1
        


        #cv.ShowImage("camera", img)
    
    
    
    
            
if __name__ == '__main__':
    captureFromCamera();
#   // if cv.WaitKey(10) == 27:
#        break
#cv.DestroyWindow("camera")