import os, shutil, time
import numpy as np
import imutils
import cv2
import pytesseract
import Image
from PIL import Image, ImageEnhance, ImageFilter
from collections import Counter
from picamera.array import PiRGBArray
from picamera import PiCamera
from stepper import Motor
from GPSDistanceConvertor import GPSXY, BearingMeet, addXY2GPS
import MAVComms

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

                #set up motor control
                self.m = Motor([18,22,24,26])                
                self.m.rpm = 5
                #set initialposition
                self.position = 0

                #declare video source for RPi
                self.resolution = {'width': 1088, 'height': 720}
                self.camera = PiCamera()
                self.camera.resolution = (self.resolution['width'], self.resolution['height'])
                self.camera.framerate = 15
                self.rawCapture = PiRGBArray(self.camera, size=(self.resolution['width'], self.resolution['height']))
                time.sleep(0.3)
        
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
                        centred = self.moveCamera(centre[0], orig.shape[1]/2)
                        return True, centred
                else:
                        return False, False

        def moveCamera(self, target_X, frame_Width):
                d_X = float(frame_Width - target_X)
                #print(d_X)
                set_Fraction = d_X/frame_Width
                #print(set_Fraction)
                #if greater than 5% left or right of centre
                if(abs(set_Fraction)>0.05):    
                        max_Setpoint = 40
                        d_Position = set_Fraction*max_Setpoint
                        #print(d_Position)
                        self.position += (set_Fraction*max_Setpoint)
                        self.m.move_to(self.position)
                        print("Setpoint = %d degrees" % self.position)
                        return False
                else:
                        print("Centred")
                        return True

        def adjustAndRecordFrame(self, frame, contours):
                warped = self.four_point_transform(frame, contours.reshape(4, 2)) #* ratio)
                #warped = cv2.bitwise_not(warped)       
                #warped = adjust_gamma.adjust_gamma(warped, 0.7)
                warped = cv2.blur(warped,(5,5))
                warped = cv2.GaussianBlur(warped,(5,5),0)
                #warped = ImageEnhance.Contrast(warped)
                #warped = enhancer.enhance(2)
                warped = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,9,1)
                #cv2.imwrite('toDetect.jpg', warped)
                img = Image.fromarray(warped)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2)

                #save the frame to be run through OCR later
                savestring = 'images/toDetect'+str(self.frameCount)+'.jpg'
                img.save(savestring)
                print 'image saved as ' + savestring

                
        def runOCR(self):
                print 'running OCR'
                for x in xrange(0, self.frameCount, 5):
                        try:
                                text= pytesseract.image_to_string(Image.open('images/toDetect'+str(x)+'.jpg'),config='-psm 10')
                        except IOError:
                                print 'file doesn\'t exist' + 'images/toDetect'+str(x)+'.jpg' 
                                #try the name file, ie next x
                                continue
                        
                        #store detected character
                        self.detectedCharacters.append(text)
        
                character =  Counter(self.detectedCharacters).most_common(1)
                if(character[0][0] != ''):
                        #print(character[0][0])
                        return(character[0][0])
                elif(len(character)>1):
                        #print(character[1][0])
                        return(character[1][0])


        def cleanImagesFolder(self):
                folder = '/home/pi/UCLR-UAS/images/'
                print("Cleaning %s" % folder)
                for the_file in os.listdir(folder):
                    file_path= os.path.join(folder, the_file)
                    try:
                        if((os.path.isfile(file_path)) and (file_path != "/home/pi/UCLR-UAS/images/placeholder")):
                                        os.remove(file_path)
                        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as e:
                            print(e)
                self.frameCount = 0

        def adjust_gamma(self, image, gamma=1.0):
                # build a lookup table mapping the pixel values [0, 255] to
                # their adjusted gamma values
                invGamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** invGamma) * 255
                        for i in np.arange(0, 256)]).astype("uint8")
         
                # apply gamma correction using the lookup table
                return cv2.LUT(image, table)

        def order_points(self, pts):
                # initialzie a list of coordinates that will be ordered
                # such that the first entry in the list is the top-left,
                # the second entry is the top-right, the third is the
                # bottom-right, and the fourth is the bottom-left
                rect = np.zeros((4, 2), dtype = "float32")

                # the top-left point will have the smallest sum, whereas
                # the bottom-right point will have the largest sum
                s = pts.sum(axis = 1)
                rect[0] = pts[np.argmin(s)]
                rect[2] = pts[np.argmax(s)]

                # now, compute the difference between the points, the
                # top-right point will have the smallest difference,
                # whereas the bottom-left will have the largest difference
                diff = np.diff(pts, axis = 1)
                rect[1] = pts[np.argmin(diff)]
                rect[3] = pts[np.argmax(diff)]

                # return the ordered coordinates
                return rect

        def four_point_transform(self, image, pts):
                # obtain a consistent order of the points and unpack them
                # individually
                rect = self.order_points(pts)
                (tl, tr, br, bl) = rect

                # compute the width of the new image, which will be the
                # maximum distance between bottom-right and bottom-left
                # x-coordiates or the top-right and top-left x-coordinates
                widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))

                # compute the height of the new image, which will be the
                # maximum distance between the top-right and bottom-right
                # y-coordinates or the top-left and bottom-left y-coordinates
                heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))

                # now that we have the dimensions of the new image, construct
                # the set of destination points to obtain a "birds eye view",
                # (i.e. top-down view) of the image, again specifying points
                # in the top-left, top-right, bottom-right, and bottom-left
                # order
                dst = np.array([
                        [0, 0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1],
                        [0, maxHeight - 1]], dtype = "float32")

                # compute the perspective transform matrix and then apply it
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

                # return the warped image
                return warped

class missionRecon:
    def __init__(self, VecConn, maxTurnAngle=60):
        if(0 <= maxTurnAngle <= 360):
            self.maxTurnAngle = maxTurnAngle
        else:
            raise ValueError('maxTurnAngle must be between 0 and 360')

        self.MAVcomms = VecConn
        self.dataCount = 0

    def detection(self):
        d = detectTarget()
        posData = {}
        for i in range(4):
            posData['target' + str(i)] = {}
            posData['target' + str(i)]['LAT'] = {}
            posData['target' + str(i)]['LONG'] = {}
            posData['target' + str(i)]['HEADING'] = {}
            try:
                for frame in d.camera.capture_continuous(d.rawCapture, format="bgr", use_video_port=True):
                        frame = frame.array
                        #cv2.imshow("Frame", frame)
                        hsv, grayscale, original = d.changeColourspace(frame)
                        frame = d.masking(hsv)
                        #cv2.imshow("Outline", frame)
                        targetContour = d.findContour(frame)
                        if(targetContour is not None):
                                targetSizenCentred = d.processContour(targetContour, original)
                                if(targetSizenCentred[0]):
                                        #if target it both appropriately size and centred
                                        if(targetSizenCentred[1]):        
                                            #get location
                                            currPos = self.MAVcomms.getGPSdata()
                                            currAtt = self.MAVcomms.getAttitude()
                                            #if(abs(self.MAVcomms.MAVData['ROLL'])<0.175 and abs(self.MAVcomms.MAVData['PITCH'])<0.175)

                                            #record data
                                            posData['target' + str(i)]['LAT'][self.dataCount] = self.MAVcomms.MAVData['LAT']
                                            posData['target' + str(i)]['LONG'][self.dataCount] = self.MAVcomms.MAVData['LONG']
                                            posData['target' + str(i)]['HEADING'][self.dataCount] =  self.MAVcomms.MAVData['YAW'] + d.position
                                            self.dataCount += 1
                                            
                                        if(d.frameCount % 5 == 0):
                                                d.adjustAndRecordFrame(grayscale[2], targetContour)

                                        d.frameCount += 1
                        else:
                                pass
                        
                        d.rawCapture.truncate(0)
                        if(abs(d.position) > abs(self.maxTurnAngle)):
                            print('Max turning angle reached')
                            break

            except KeyboardInterrupt:
                pass
            #cv2.destroyAllWindows()
            d.m.move_to(0)
            posData['target' + str(i)]['detectedChar'] = d.runOCR()
            d.cleanImagesFolder()
            time.sleep(2)

            self.dataCount = 0
            #delete this break for production version (so it runs 4 times)
            break
	    print('target' + str(i))
        d = None
        missionRecon.recordDatatoFile(self, posData)
        avg_lat, avg_long = missionRecon.calculation(self, posData, str(i))

        print avg_lat, avg_long, posData['target' + str(i)]['detectedChar']


    def calculation(self, targetData, targetNo):
        print('Starting calculation')
        strTarget = 'target' + str(targetNo)
        originLAT = targetData[strTarget]['LAT'][0]
        originLONG = targetData[strTarget]['LONG'][0]    
        xyMatrix = []
        data_counter = 0
        for i in range(len(targetData[strTarget]['LAT'])):
            currLAT = targetData[strTarget]['LAT'][i]
            currLONG = targetData[strTarget]['LONG'][i]
            currHEADING = targetData[strTarget]['HEADING'][i]
            for j in range(len(targetData[strTarget]['LAT'])):
                if(i == j):
                    xyMatrix.append([])
                    xyMatrix[data_counter].append(0)
                    xyMatrix[data_counter].append(0)
                else:
                    compLAT = targetData[strTarget]['LAT'][j]
                    compLONG = targetData[strTarget]['LONG'][j]
                    compHEADING = targetData[strTarget]['HEADING'][j]
                    XY1 = GPSXY(originLAT, originLONG, currLAT, currLONG)
                    XY2 = GPSXY(originLAT, originLONG, compLAT, compLONG)
	            #print(XY1, XY2, currHEADING, compHEADING)
                    targetXY = BearingMeet(XY1[0], XY1[1], XY2[0], XY2[1], currHEADING, compHEADING)
                    if(targetXY[0] is not None and targetXY[1] is not None):
                        GPSestimate = addXY2GPS(originLAT, originLONG, targetXY[0], targetXY[1])
                        xyMatrix.append([])
                        xyMatrix[data_counter].append(GPSestimate[0])
                        xyMatrix[data_counter].append(GPSestimate[1])
                    else:
                        #print targetXY
                        xyMatrix.append([])
                        xyMatrix[data_counter].append(0)
                        xyMatrix[data_counter].append(0)
                data_counter += 1

        #average GPS values, first stripping zeros
        total_lat = 0
        total_long = 0
        data_count = 0
	#print xyMatrix
        for i in range(len(xyMatrix)):
            if(xyMatrix[i][0] == 0):
                pass
            else:
                total_lat += xyMatrix[i][0]
                total_long += xyMatrix[i][1]
                data_count += 1

        if(data_count == 0):
            print("No data recorded")
            return None, None

        avg_lat = total_lat / (data_count)
        avg_long = total_long / (data_count)

        return avg_lat, avg_long


    def recordDatatoFile(self, data):
        with open('log.txt', 'w') as f:
            for key, value in data.items():
                f.write('%s:%s\n' % (key, value))


def main():
	print('Starting MAV connection')
	m = MAVComms.MAVconnect('/dev/ttyACM0')
        if(m.vehicle is not None):
                print('Initialising mission object')
                mission = missionRecon(m)
                print('Starting detection')
                mission.detection()
        else:
                print('No connection, exiting')
		

def main1():
        d = detectTarget()
        #PC Version
        #while True:
                #(grabbed, frame) = d.camera.read()
        #RPi Version
        try:
	        for frame in d.camera.capture_continuous(d.rawCapture, format="bgr", use_video_port=True):
        	        frame = frame.array
                	#cv2.imshow("Frame", frame)
	                hsv, grayscale, original = d.changeColourspace(frame)
	                frame = d.masking(hsv)
	                #cv2.imshow("Outline", frame)
       	        	targetContour = d.findContour(frame)
                	if(targetContour is not None):
                	        if(d.processContour(targetContour, original)):
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
        except KeyboardInterrupt:
		pass
        #cv2.destroyAllWindows()
        d.m.move_to(0)
        print(d.runOCR())
        d.cleanImagesFolder()
        time.sleep(3)
        d = None
        
        
        
#if module is being run stand alone, run the following
if __name__ == "__main__":
        print 'running stand alone'
        main()
