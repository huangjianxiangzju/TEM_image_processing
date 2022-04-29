# -*- coding: utf-8 -*-
# Reference 1: https://blog.csdn.net/jkwwwwwwwwww/article/details/70195508
# Reference 2: Image processing and acquisition using python
import numpy as np
import scipy.ndimage
from PIL import Image
import scipy.misc, cv2
import sys
import imageio
import os


def detectContour(imagefile):
    # opening the image and converting it to grayscale
    a = Image.open(imagefile).convert('L') 
    # convert the image to numpy matrice
    a = scipy.misc.fromimage(a)
    # further convert and clip the numpy array   
    b=a>100  # element greater than 100--->True,less or equal than 100--->False
    b1=scipy.misc.toimage(b[:890]) #get rid of the black bar 
    # save the processed image
    name=imagefile.split('.',1)[0]
    file1=name+'_preprocessed.png'
    b1.save(file1)
    
    #use the cv2 module to process the preprocessed image
    img = cv2.imread(file1)
    # Img to Grey
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
    # Grey to Binary
    ret, binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)  
    # Detect the contours
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  

    # For each detected contour, contour line was drawn for visualiszation
    # and output the area to the file
    file2=name+'.dat'
    ofile=open(file2,'w')
    i=1
    file_names=[]
    #make a directory to store the images
    os.system('md '+name)
    for contour in contours:
        # the lower limit 40; the upper limit 100000
        if (cv2.contourArea(contour)>40 and cv2.contourArea(contour)<100000):
            #write the file
            ofile.write(str(i)+"\t")
            ofile.write(str(cv2.contourArea(contour))+'\n')
        			# '/(40.5**2)' transform the pixel square to nanometer square.
            #save the corresponding image
#            print ('Caution:  the area unit is nanometer square!')
            cv2.drawContours(img,contour,-1,(0,0,255),3)
            cv2.imwrite('./'+name+'/'+name+str(i)+'.png',img)
            file_names.append('./'+name+'/'+name+str(i)+'.png')
#            cv2.imshow("img", IMG)  
            cv2.waitKey(0)
            i=i+1 
    ofile.close()
    print ('The drawn contours were finished.')

    #generate a gif for inspection
    with imageio.get_writer(name+'.gif', mode='I') as writer:
        for filename in file_names:
            image = imageio.imread(filename)
            writer.append_data(image)

if __name__=="__main__":
    if sys.argv[1]=='all':
        dirlist=os.listdir(os.getcwd())
        for pic in dirlist:
            if ".tif" in pic:
                detectContour(pic)
                print pic
    else:
        detectContour(sys.argv[1])