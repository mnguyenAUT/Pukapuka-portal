import cv2, os
import numpy as np
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt
import random
from readQR import *

def runAll(letter):
    setTestRandomDot(True)
    
    os.system('python createQR.py \"E Ihowā Atua, O ngā iwi mātou rā, Āta whakarangona, Me aroha noa, Kia hua ko te pai, Kia tau tō atawhai, Manaakitia mai, Aotearoa.\" '+letter)
      
    for cover in range(10, 80, 10):
        setTestRandomDotCoverPercentage(cover)    
        print("QR Code Cover = "+str(cover))
        counter = 0
        
        for x in range(111):
            image = cv2.imread("qr.png")  
            obj = decodeColourQR(image)
            if obj:
                counter = counter + 1
        print ("Accuracy: "+str(round(100*counter/111,2)) + "%")
        
        print("Colour QR Code Cover = "+str(cover))
        counter = 0
        for x in range(111):
            image = cv2.imread("qr_Colour.png")  
            obj = decodeColourQR(image)
            if obj:
                counter = counter + 1
        print ("Accuracy: "+str(round(100*counter/111,2)) + "%")

if __name__ == '__main__':
    
    argument = "L"
    if len(sys.argv) > 1:
        argument = sys.argv[1]
    print ("**********************\nExperiments for "+argument)    
    runAll(argument)  