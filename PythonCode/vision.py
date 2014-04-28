import cv2
import numpy as np

img = cv2.imread("mars.png",0)
img = cv2.medianBlur(img,11)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT,1.1,100,
                        param1=50,param2=30,minRadius=10,maxRadius=20)

circles = np.uint16(np.around(circles))


for i in circles[0,:]:
	cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
	cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
