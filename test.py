import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def get_number_features(img1,img2):
	img1 = cv.imread(img1,0)          # queryImage
	img2 = cv.imread(img2,0) # trainImage
	#img1=cv.resize(img1,(512,512))
	#img2=cv.resize(img2,(512,512))
	# 1) Check if 2 images are equals
	# Initiate SIFT detector
	sift = cv.xfeatures2d.SIFT_create()
	# find the keypoints and descriptors with SIFT
	kp1, des1 = sift.detectAndCompute(img1,None)
	kp2, des2 = sift.detectAndCompute(img2,None)
	# BFMatcher with default params
	bf = cv.BFMatcher()
	matches = bf.knnMatch(des1,des2, k=2)
	# Apply ratio test
	good = []
	for m,n in matches:
	    if m.distance < 0.75*n.distance:
	        good.append([m])
	# cv.drawMatchesKnn expects list of lists as matches.
	img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,img1,flags=2)
	
	#plt.imshow(img3),plt.show()

	return len(good)