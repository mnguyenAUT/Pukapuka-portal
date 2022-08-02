import requests, os, sys
import cv2
import urllib.request
import numpy as np
import math  
from urllib.request import urlopen
url = 'https://instructionalseries.tki.org.nz/Instructional-Series/Junior-Journal/Junior-Journal-51-Level-2-2015/Living-in-a-Colourful-World'
url = 'https://instructionalseries.tki.org.nz/Instructional-Series/Junior-Journal/Junior-Journal-60-Level-2-2020/Super-Shells'
if len(sys.argv) > 1:
	url = sys.argv[1]

html = urlopen(url).readlines()
jpgURL = ""
for line in html: 
    stringLine = line.decode("utf-8") 
    #print(stringLine)
    if True:
        if "_resource_image.jpg" in stringLine: 
            indexA = stringLine.find("src=")        
            indexB = stringLine.find("_resource_image.jpg")        
            jpgURL = "https://instructionalseries.tki.org.nz/"+stringLine[indexA+5: indexB+19]
            print(jpgURL)
        
        elif "pdf-ico" in stringLine:        
            indexA = stringLine.find("href=")        
            indexB = stringLine.find(".pdf")        
            pdfURL = "https://instructionalseries.tki.org.nz/"+stringLine[indexA+6: indexB+4]
            print(pdfURL)
            r = requests.get(pdfURL, stream=True)
            with open('./temp.pdf', 'wb') as fd:
                for chunk in r.iter_content(10000):
                    fd.write(chunk)
            os.system('del *.ppm')
            os.system("pdfToImage.bat")
            
            imagePDF = cv2.imread("image.ppm")
            heightOrig = int(imagePDF.shape[0])
            widthOrig = int(imagePDF.shape[1])
            if widthOrig > 1.2*heightOrig:
                n_white_pix_left = np.sum(imagePDF[:,0:int(widthOrig/2)] > 250)
                n_white_pix_right = np.sum(imagePDF[:,0:int(widthOrig/2)] < 250)
                #print(n_white_pix_left)
                #print(n_white_pix_right)
                #print(math.floor(widthOrig/2))
                #print(math.floor(widthOrig/2)+math.floor(widthOrig/2))
                if n_white_pix_left > 10*n_white_pix_right:
                    imagePDF[:,0:math.floor(widthOrig/2)]=imagePDF[:,math.floor(widthOrig/2):math.floor(widthOrig/2)+math.floor(widthOrig/2)]
            
            #percent by which the image is resized
            scale_percent = 100*800/heightOrig

            #calculate the 50 percent of original dimensions
            width = int(imagePDF.shape[1] * scale_percent / 100)
            height = int(imagePDF.shape[0] * scale_percent / 100)

            # dsize
            dsize = (width, height)

            # resize image
            imagePDF = cv2.resize(imagePDF, dsize)
            if imagePDF.shape[1] > 800:
                cv2.imwrite("image.ppm", imagePDF[0:800,0:600])
            else:
                cv2.imwrite("image.ppm", imagePDF)

            
            break
            
        elif "tsm-ico" in stringLine:             
            print(jpgURL)
            req = urllib.request.urlopen(jpgURL)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1) # 'Load it as it is'
            im_v = cv2.vconcat([img, img])
            im_h = cv2.hconcat([im_v, im_v])
            scale_percent = 450 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(im_h, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite('image.ppm', resized)
            