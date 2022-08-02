#Ready-to-Read-Phonics-Plus = RRPP = 29181
#Ready-to-Read-Colour-Wheel = RRCW = 22576
#Junior Journal = JJ = 22577
#School Journal = SJ = 22578

import cv2, io
import requests, os, sys
import PySimpleGUI as sg
from PIL import Image
import time

# Resize PNG file to size (300, 300)
size = (700, 800)
im = cv2.imread("finalQR.png")
im = cv2.resize(im, size)
cv2.imwrite("temp.png", im)

# Using readlines()
#file1 = open('readingLists/level1.txt', 'r')
#Lines = file1.readlines()
#count = 0
# Strips the newline character
#for line in Lines:
urlValue = sys.argv[1]
folderValue = sys.argv[2]
    #print(urlValue)
    #break
urlValue_short = urlValue.replace("https://instructionalseries.tki.org.nz/Instructional-Series/", "")
urlValue_short = urlValue_short.replace("Ready-to-Read-Phonics-Plus", "RRPP")
urlValue_short = urlValue_short.replace("Ready-to-Read-Colour-Wheel", "RRCW")
urlValue_short = urlValue_short.replace("Junior-Journal", "JJ")
urlValue_short = urlValue_short.replace("School-Journal", "SJ")
print (urlValue_short)
splitted = urlValue.split("/")
        
os.system("python pdf2Image.py \""+str(urlValue)+"\"")
os.system("python createQRTag.py \"cerv.aut.ac.nz/tki/?u="+str(urlValue_short)+"\"")

im = cv2.imread("finalQR.png")
if splitted[-1] != "":
    cv2.imwrite("outputs/"+str(folderValue)+"/"+splitted[-1]+".png", im)
im = cv2.resize(im, size)
cv2.imwrite("temp.png", im)  

