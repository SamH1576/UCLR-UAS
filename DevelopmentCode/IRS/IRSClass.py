import os, shutil, time
import transform
import numpy as np
import imutils
import cv2
import pytesseract
import Image
import adjust_gamma
from PIL import Image, ImageEnhance, ImageFilter
from collections import Counter
from picamera.array import PiRGBArray
from picamera import PiCamera

class detectTarget:
        def __init__(self):
                #declare list for detected characters
                self.detectedCharacters = []
                #declare frame counter
                self.frameCount = 0
                #declare bounds for detection colours
                self.redLower1 = (0,100,100)
                self.redUpper1 = (10,255,255)
		self.redLower2 = (170,100,100)
		self.redUpper2 = (180,255,255)
                #declare video source for PC
                #self.camera = cv2.VideoCapture(0)

                #declare video source for RPi
                self.camera = PiCamera()
                self.camera.resolution = (640, 480)
                self.camera.framerate = 10
                self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
                time.sleep(0.2)
        
        def changeColourspace(self, rbgImage):
                #convert to hsv
                hsv = cv2.cvtColor(rbgImage, cv2.COLOR_BGR2HSV)
                #convert to grayscale - note grayscale[2] is used
                grayscale = cv2.split(hsv)
                #return copy of original
                original = rbgImage
                return hsv, grayscale, original
        
        def masking(self, frame):
                #blur the image, gaussian for guassian noise
                frame = cv2.GaussianBlur(frame,(3,3), 0)
                #- median blur for salt and pepper noise
                frame = cv2.medianBlur(frame, 5)
                #drop pixels out of range
                mask1 = cv2.inRange(frame, self.redLower1, self.redUpper1)
		mask2 = cv2.inRange(frame, self.redLower2, self.redUpper2)
		frame = mask1 + mask2 
                #erode
                frame = cv2.erode(frame, None, iterations=2)
                #dilate
                frame = cv2.dilate(frame, None, iterations=1)
                return frame
        
        def findContour(self, frame):
                screenCnt = None
                #find contours, and order by size, largest first
                (cnts, _) = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
                #go over contours and find four sided contour
                for c in cnts:
                        # approximate the contour
                        peri = cv2.arcLength(c, True)
                        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                        # if our approximated contour has four points, then we
                        # can assume that we have found our box
                        if len(approx) == 4:
                                screenCnt = approx
                                break
                #return the contour geometry is screenCnt set
                if(screenCnt is not None):
                        return screenCnt
                else:
                        return None

        def processContour(self, contour, orig):
                #calculate moments
                M = cv2.moments(contour)
                #determine centroid and area
                centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                area = M["m00"]
                if(area>200):
                        if(centre[0]>(orig.shape[1]/2)): 
                                #move camera right
                                print("Move right")
                        else:
                                #move camera left
                                print("Move left")
                        return True
                else:
                        return False
                                
        def adjustAndRecordFrame(self, frame, contours):
                warped = transform.four_point_transform(frame, contours.reshape(4, 2)) #* ratio)
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

                #save the frame to be run through OCR later
                savestring = 'DevelopmentCode/IRS/images/toDetect'+str(self.frameCount)+'.jpg'
                img.save(savestring)
                print 'image saved as ' + savestring
                
                
        def runOCR(self, cleanUp):
                print 'running OCR'
                for x in xrange(0, self.frameCount, 5):
                        try:
                                text= pytesseract.image_to_string(Image.open('DevelopmentCode/IRS/images/toDetect'+str(x)+'.jpg'),config='-psm 10')
                        except IOError:
                                print 'file doesn\'t exist' + 'images/toDetect'+str(x)+'.jpg' 
                                #try the name file, ie next x
                                continue
                        
                        #store detected character
                        self.detectedCharacters.append(text)
        
                character =  Counter(self.detectedCharacters).most_common(1)
                if(character[0][0] != ''):
                        print(character[0][0])
                elif(len(character)>1):
                        print(character[1][0])
                
                if(cleanUp):
                        cleanImagesFolder()
                        self.frameCount = 0
                        
        def cleanImagesFolder():
                folder = 'images'
                for the_file in os.listdir(folder):
                        file_path= os.path.join(folder, the_file)
                try:
                        if os.path.isfile(file_path):
                                        os.unlink(file_path)
                        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                        print(e)
                

def main():
        d = detectTarget()
        #PC Version
        #while True:
                #(grabbed, frame) = d.camera.read()
        #RPi Version
        for frame in d.camera.capture_continuous(d.rawCapture, format="bgr", use_video_port=True):
                frame = frame.array
                cv2.imshow("Frame", frame)
                hsv, grayscale, original = d.changeColourspace(frame)
                frame = d.masking(hsv)
                cv2.imshow("Outline", frame)
                targetContour = d.findContour(frame)
                if(targetContour is not None):
                        if(d.processContour(targetContour, original)):
                                pass
                                if(d.frameCount % 5 == 0):
                                        d.adjustAndRecordFrame(grayscale[2], targetContour)
                                d.frameCount += 1
                else:
                        pass

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                        break
                #for RPI only
                d.rawCapture.truncate(0)
        
        cv2.destroyAllWindows()
        d.runOCR(False)
        d = None
        
        
#if module is being run stand alone, run the following
if __name__ == "__main__":
        print 'running stand alone'
        main()
