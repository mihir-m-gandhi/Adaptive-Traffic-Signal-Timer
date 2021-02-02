import numpy as np
import cv2

image = cv2.imread('test4.jpg')
cv2.imshow('actual image',image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscaled',gray)
thr = gray
ret,thr = cv2.threshold(gray,90,255,cv2.THRESH_BINARY)	#threshold value need to be set
cv2.imshow('binary',thr)
count = cv2.countNonZero(thr)
total = thr.size
density = (total-count)/total
print("Traffic density is",density)
cv2.waitKey(0)
cv2.destroyAllWindows()