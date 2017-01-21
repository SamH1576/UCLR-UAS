import cv2

camera = cv2.VideoCapture(0)

(grabbed, frame) = camera.read()

cv2.imwrite("image1.png", frame)
