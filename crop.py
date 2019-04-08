import cv2
import numpy as np
#img = cv2.imread("test.png")

def crp(imgtocrop):
	img = cv2.imread(imgtocrop)
	img=cv2.resize(img,(512,512))
	blurred = cv2.blur(img, (3,3))
	canny = cv2.Canny(blurred, 50, 200)

	## find the non-zero min-max coords of canny
	pts = np.argwhere(canny>0)
	y1,x1 = pts.min(axis=0)
	y2,x2 = pts.max(axis=0)
	saved_img="ccc"+imgtocrop
	## crop the region
	cropped = img[y1:y2, x1:x2]
	cv2.imwrite(saved_img, cropped)

	tagged = cv2.rectangle(img.copy(), (x1,y1), (x2,y2), (0,255,0), 3, cv2.LINE_AA)
	cv2.imshow("tagged", tagged)
	cv2.waitKey(2000)