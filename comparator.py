import sys,os
from test import get_number_features

def identify_fingerprint():
	names=[]
	means=[]

	for x in os.listdir("./static/images"):
		if x !=".DS_Store":
			img1=os.path.join("./static/images",x)
			print(img1)
			break 

	for foldername in os.listdir("./people"):
		if foldername !=".DS_Store":
			print(foldername)
			sum=0
			i=0
			for img in os.listdir("./people/"+foldername):
				if img !=".DS_Store":
					y="./people/"+os.path.join(foldername,img)
					print(y)
					i=i+1
					sum=sum+get_number_features(img1,y)
			mean=sum
			print(mean)
			names.append(foldername)
			means.append(mean)

	print(names)
	print(means)

	Z = [x for _,x in sorted(zip(means,names))]	
	print(Z)
	print("the fingerprint is from "+str(Z[len(Z)-1]))
	y="the fingerprint is from "+str(Z[len(Z)-1])

	return y 
				



        	


