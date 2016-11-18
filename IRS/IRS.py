import transform
import numpy as np
import argparse
import imutils
import cv2
import pytesseract
import Image
import adjust_gamma

# Colour detection bounds
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
redLower = (0,100,100)
redUpper = (10,255,255)

# For dev this is webcam, on RPi this will be different
camera = cv2.VideoCapture(0)

# For live testing
while True: 
	(grabbed, frame) = camera.read()

	# Keep copy of original and the ratio 
	#ratio = frame.shape[1] / 600.0
	orig = frame.copy()
	#frame = imutils.resize(frame, width=600)

	#cv2.imshow("Image", frame)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#grayscale = cv2.split(hsv)
	#Clear up image
	mask = cv2.inRange(hsv, redLower, redUpper)
	#cv2.imshow("Mask", mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=4)


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

	try:
		screenCnt
		# Calculate Moments and determine centroid
		M = cv2.moments(screenCnt)
		centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	 	area = M["m00"]
		print(area)
		if(area>400):	
			if(centre[0]>(frame.shape[0]/2)):
				print("Move right")
			else:
				print("Move left")
			cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)
			cv2.imshow("Outline", frame)

			warped = transform.four_point_transform(orig, screenCnt.reshape(4, 2)) #* ratio)
			warped = cv2.bitwise_not(warped)
			warped = adjust_gamma.adjust_gamma(warped, 0.7)
			#ret, warped = cv2.threshold(warped, 127,255, cv2.THRESH_BINARY)
			cv2.imwrite('toDetect.png', warped)
			cv2.imshow("warped", warped)
			text = pytesseract.image_to_string(Image.open('toDetect.png'),config='-psm 10')
			print(text)
		else:
			print("No box found")
	except NameError:
		print("No box found")
		exit

	cv2.imshow("Outline", frame)

	# if the 'q' key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	

#	cv2.waitKey(0)
#	cv2.destroyAllWindows()

camera.release()
cv2.destroyAllWindows()


