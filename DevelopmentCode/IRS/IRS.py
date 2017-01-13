import transform
import numpy as np
import argparse
import imutils
import cv2
import pytesseract
import Image
import adjust_gamma
from PIL import Image, ImageEnhance, ImageFilter
from collections import Counter

# Colour detection bounds
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
redLower = (0,100,100)
redUpper = (10,255,255)

# For dev this is webcam, on RPi this will be different
camera = cv2.VideoCapture(0)

# Initialise screenCnt so we can check it later
screenCnt = None

# New list for detected characters
pyCharacter = []

# For live testing
while True: 
        (grabbed, frame) = camera.read()

        # Keep copy of original and the ratio 
        #ratio = frame.shape[1] / 600.0
        orig = frame.copy()
        #frame = imutils.resize(frame, width=600)

        #cv2.imshow("Image", frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        grayscale = cv2.split(hsv)
        #blur image
        hsv = cv2.GaussianBlur(hsv,(3,3), 0)
        hsv = cv2.medianBlur(hsv, 5)
        #Clear up image
        mask = cv2.inRange(hsv, redLower, redUpper)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=1)
        cv2.imshow("Mask", mask)
        
        # Grab contours
        (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]


        # loop over the contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # if our approximated contour has four points, then we
                # can assume that we have found our box
                if len(approx) == 4:
                        screenCnt = approx
                        break

        if(screenCnt is not None):      
                # Calculate Moments and determine centroid
                M = cv2.moments(screenCnt)
                centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                area = M["m00"]
                #print(area)
                if(area>200):   
                        if(centre[0]>(orig.shape[1]/2)): #THIS MAY NOT BE RIGHT centre[0] -> centre
                                print("Move right")
                        else:
                                print("Move left")
                        cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)
                        cv2.circle(frame, (centre[0], centre[1]), 7, (255, 255, 255), -1)
                        cv2.imshow("Outline", frame)

                        warped = transform.four_point_transform(grayscale[2], screenCnt.reshape(4, 2)) #* ratio)
                        #warped = cv2.bitwise_not(warped)       
                        #warped = adjust_gamma.adjust_gamma(warped, 0.7)
                        warped = cv2.GaussianBlur(warped,(5,5),0)
                        #warped = ImageEnhance.Contrast(warped)
                        #warped = enhancer.enhance(2)
                        warped = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
                        #cv2.imwrite('toDetect.jpg', warped)
                        img = Image.fromarray(warped)
                        enhancer = ImageEnhance.Contrast(img)
                        img = enhancer.enhance(2)
                        cv2.imshow("warped", warped)
                        #text = pytesseract.image_to_string(Image.open('toDetect.jpg'),config='-psm 10')
                        #send img to OCR, -psm 10 tells the OCR to look for a single character
                        text = pytesseract.image_to_string(img,config='-psm 10')
                        
                        #add the detected character to the list
                        pyCharacter.append(text)
                        #print(text)
                else:
                        print("Area too small")
                        pass
        else:
                print("No box found")
                exit

        cv2.imshow("Outline", frame)
        
        #reset screenCnt
        screenCnt = None

        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                break

character = Counter(pyCharacter).most_common(1)
print(character[0][0])

#       cv2.waitKey(0)
#       cv2.destroyAllWindows()

camera.release()
cv2.destroyAllWindows()

###############################
# Dev Section
###############################

#code outline
#############

#class targetDetection: 
#set parameters (like detection bounds, frame size, connection), declare detection array and screenCnt

#grab frame
#do geometric steps (reduce size, keep original etc)
#change colourspace
#blur
#mask
#erode
#dilate
#find contours
#sort contours by size
#attempt to fit largest contour to straight lines
#if it has four edges then it is probably target
#determine area bounded by contour and its centroid
#if large enough, check location
#warp contour area to a square
#blur again
#threshold (increase contrast)
#send the area to py tesseract for OCR
#store the result
