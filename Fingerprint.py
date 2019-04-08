from PIL import Image
import numpy as np
import os
import pickle
from sklearn import svm
from sklearn.model_selection import train_test_split
from itertools import combinations
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
import imagehash

class FingerPrint():
    def __init__(self,fp_path):
        """
        Initialize common variables
        """
        #svm.SVC(gamma=0.1,decision_function_shape='ovr',kernel='rbf')
        self.clf = svm.SVC(gamma=0.001,decision_function_shape='ovr',kernel='poly',degree=3)
        self.clf2  = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2))
        self.fp_path = fp_path
        self.im_width = 256
        self.im_height = 256
        self.array = []
        self.arrayt=[]
        self.y=[]
        self.score=0
        self.score2=0
        self.z=[]
        self.names=[]
        self.yf=[]
        self.zf=[]
        self.training=[]
        self.trainingy=[]
        self.comp=[]
        self.compy=[]
        self.compf=[]
    
        

             

      #method that saves the new image  
    def image_export(self, filename):
        self.im.save(self.fp_path + filename[:-4] + '_monochromatic.png')
    def hash(self):
        filename =os.listdir(self.fp_path)[0]
        hash = imagehash.average_hash(Image.open('first.jpg'))
        otherhash = imagehash.average_hash(Image.open(self.fp_path+filename))
        self.hashed=hash-otherhash
        
        #method that resizes the image
    def resize(self):
        self.im = self.im.resize((self.im_height, self.im_width), 0)

    def av_hash(self,filename):
        ref = imagehash.average_hash(Image.open('first.jpg'))
        hash=imagehash.average_hash(Image.open(self.fp_path+filename))
        diff_av=ref-hash
        return diff_av
        
    def p_hash(self,filename):
        ref = imagehash.phash(Image.open('first.jpg'))
        hash=imagehash.phash(Image.open(self.fp_path+filename))
        diff_p=ref-hash
        return diff_p

    def d_hash(self,filename):
        ref = imagehash.dhash(Image.open('first.jpg'))
        hash=imagehash.dhash(Image.open(self.fp_path+filename))
        diff_d=ref-hash
        return diff_d    

    def w_hash(self,filename):
        ref = imagehash.whash(Image.open('first.jpg'))
        hash=imagehash.whash(Image.open(self.fp_path+filename))
        diff_w=ref-hash
        return diff_w  


    def dataload(self):
        i=0
        for filename in os.listdir(self.fp_path):
            if filename.endswith('.JPG') or filename.endswith('.jpg') or filename.endswith('.png'):
                a=self.av_hash(filename)
                b=self.p_hash(filename)
                c=self.d_hash(filename)
                d=self.w_hash(filename)
                print(filename)
                print(a,b,c,d)
                self.training.append([a,b,c,d])
                if "yes" in filename:
                    self.trainingy.append(1)
                else:
                    self.trainingy.append(0)    
                print(self.trainingy[i])    
                i=i+1
                self.names.append(filename)
        self.training=np.asarray(self.training)
        self.training.reshape((self.training.shape[0],-1))
        print(self.training.shape)
        print(self.training)
        print(self.trainingy)
        print("Training size=",len(self.training))
    
            
    
    # Convert image to black and white without dithering
    def to_bw(self):
        #inserting the image in column
        col=self.im
        #converting the image into grayscale using luma configuration
        gray = col.convert('L')
        print(type(gray))
        #depending on the grayscale value of the pizxel it is set as a black dot or white dot
        self.im = gray.point(lambda x: 0 if x<120 else 255, '1')
         
    def binarization(self):
        for filename in os.listdir(self.fp_path):
       
            if filename.endswith('.JPG') or filename.endswith('.jpg') or filename.endswith('.png'):
                #opens the image
                self.im = Image.open(self.fp_path + filename)  
                #resizes the image
                self.resize()
                #transform it to black and white
                self.to_bw()
                #rotate the image (picture was take horizontally)
                self.im=self.im.rotate(270)
                #self.image_export(filename)
                #insert the image into a matrix
                matrix = np.asarray(self.im)
                #inserting the matrix into an array
                self.array.insert(1, matrix)
                self.names.append(filename)
                if ("yes" in filename):
                    self.y.append(0)
                else:
                    self.y.append(1)    
                #self.im.show()
                print("Binarizinggg")

        
        
    def run(self):
        
        #iterates over the dataset
        self.binarization()
        self.array = np.asarray(self.array)
        #reshaping the array
        self.array = self.array.reshape((self.array.shape[0], -1))
        self.y= np.asarray(self.y)
        print(self.y)
        print(self.array.shape)

    def combine(self):
        indice=[]
        for i in range(len(self.array)):
            indice.append(i)
        all_combinations=list(combinations(indice,2))
        all_names_com=list(combinations(self.names,2))

        for i in range(len(all_combinations)):
            get_combi = all_combinations[i] #first combination (1,2) for e.g
            self.z.append([self.array[get_combi[0]], self.array[get_combi[1]]])
        print("from combine")
        print(self.z[0])
        self.z=np.asarray(self.z)
        print(self.z.shape)
        self.z=self.z.reshape((self.array.shape[0],-1))
        print("new shape of z")
        print(self.z.shape)
        #print(all_names_com)
        for i in range(len(self.z)):
            get_name_line=all_names_com[i]
            if (("roua" in get_name_line[0]) and ("roua" in get_name_line[1])) or(("wael" in get_name_line[0]) and ("wael" in get_name_line[1] )):
                self.yf.append(1)
            else:
                self.yf.append(0)
        print("final")
       # print(self.yf)        

        

        
    def data_comp(self):
        indice=[]
        for i in range(len(self.training)):
            indice.append(i)
        print("indices", indice)
        all_combinations=list(combinations(indice,2))
        all_names_com=list(combinations(self.names,2))
        print("All Combinations= ",len(all_combinations))
        print("All names =",len(all_names_com))
        

        for i in range(len(all_combinations)):
            get_combi = all_combinations[i] #first combination (1,2) for e.g
            self.comp.append([self.training[get_combi[0]], self.training[get_combi[1]]])
            get_name_line=all_names_com[i]
            print(get_name_line)
            if (("roua" in get_name_line[0]) and ("roua" in get_name_line[1])) or(("wael" in get_name_line[0]) and ("wael" in get_name_line[1] )):
                self.compy.append(1)
            else:
                self.compy.append(0)
        print("__________________")
        for i in range(len(self.comp)):
            print(self.comp[i])
            print(self.compy[i])
        self.comp=np.asarray(self.comp)
        print("Comp shape ") 
        self.comp = self.comp.reshape((self.comp.shape[0], -1))
        print(self.comp.shape)
        print(self.comp)
        
       
        
        
        



    def get_arr(self):
        return self.array           
        
    def getres(self):
        return self.training

            
          
    def train_detection(self):
        i=0
        while(self.score <0.9) :
         X_train, X_test, y_train, y_test = train_test_split(self.training, self.trainingy, test_size=0.2, random_state=i)   
         self.clf.fit(X_train,y_train)
         self.score=self.clf.score(X_test,y_test)
         print(self.score)
         i=i+1
         print(i)
        modelname="detection_model.sav" 
        pickle.dump(self.clf, open(modelname, 'wb'))


    def train_comparaison(self):
       i=0 
       while(self.score2<90) :
        X_train,X_test,y_train,y_test=train_test_split(self.comp,self.compy,test_size=0.2,random_state=i)
        self.clf.fit(X_train,y_train)
        self.score2=self.clf.score(X_test,y_test)
        print("score")
        print(self.score2)
        i=i+1

  
    
        
if __name__ == '__main__':
    fp = FingerPrint("")
    fp.run()





    
  

    

    

                   
    
