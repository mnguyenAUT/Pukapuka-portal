import cv2, sys, os
import numpy as np
from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt
import random
import math 
sift = cv2.SIFT_create()
kernel = np.ones((3,3),np.uint8)
TEST_RANDOM_DOT = False
DISPLAY = True
SAVE_VIDEO = False
COVER = 5 #percentage
DEBUG = True

def setTestRandomDot(setValue):
    global TEST_RANDOM_DOT 
    TEST_RANDOM_DOT = setValue
    
def setTestRandomDotCoverPercentage(setValue):
    global COVER 
    COVER = setValue
    
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def matchImage(img1, img2):
    img2 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)  
    MIN_MATCH_COUNT = 0    
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    FLANN_INDEX_KDTREE = 2
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 5)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.5*n.distance:
            good.append(m)
            
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)   
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    # Warp source image to destination based on homography
    #img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    #img3 = cv2.drawMatches(cv2.imread("b_rotated.png"),kp1,cv2.imread("r_rotated.png"),kp2,good,None,**draw_params)
    #cv2.imwrite("matches.png", img3)
    #cv2.imshow("matches.png", img3)
    #cv2.waitKey(0)
    im_out = cv2.warpPerspective(img1, M, (img2.shape[1],img2.shape[0]))
    return im_out

def decodeColourQR(image):  
  height, width, depth = image.shape  
  if TEST_RANDOM_DOT:
    #length = int(COVER*width/100)
    
    length = int(math.sqrt((COVER/100)*width*width))
    #print(COVER)
    #print(length)
    x1 = random.randint(0,width - length)
    y1 = random.randint(0,height - length)
    x2 = x1 + length
    y2 = y1 + length
    #image = cv2.circle(image, (random.randint(0,width), random.randint(0,height)), int(COVER*width/100), [128,128,128], -1)
    image = cv2.rectangle(image, (x1, y1), (x2, y2), (random.randint(0,255),random.randint(0,255),random.randint(0,255)), -1)
    #cv2.imshow("image", image)
    #cv2.waitKey(1000)
  
  # decodedObjects=pyzbar.decode(image)
  # for obj in decodedObjects: 
    # if obj is not None:
        # return obj
            
  decodedObjects = []
  checkImages = []
  
  checkImages.append(image)
     
  #width = image.shape[1]
  #height = image.shape[0]     
  #emptyImg = np.zeros((height,width), dtype=np.uint8)   
  image = increase_brightness(image)
  
  # colorReduce()
  div = 32
  image = image // div * div + div // 2 
  
  
   
  b,g,r = cv2.split(image)  
  if DEBUG:
      imageB = cv2.cvtColor(b,cv2.COLOR_GRAY2RGB)
      imageB[:, :, 1] = 0
      imageB[:, :, 2] = 0
      cv2.imwrite("b.png", imageB)
      
      imageG = cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)
      imageG[:, :, 0] = 0
      imageG[:, :, 2] = 0
      cv2.imwrite("g.png", imageG)
      
      imageR = cv2.cvtColor(r,cv2.COLOR_GRAY2RGB)
      imageR[:, :, 0] = 0
      imageR[:, :, 1] = 0
      cv2.imwrite("r.png", imageR)
  
  g = cv2.rotate(g, cv2.ROTATE_90_COUNTERCLOCKWISE)
  b = cv2.rotate(b, cv2.cv2.ROTATE_90_CLOCKWISE)  
  
  if DEBUG:
      imageB = cv2.cvtColor(b,cv2.COLOR_GRAY2RGB)
      imageB[:, :, 1] = 0
      imageB[:, :, 2] = 0
      cv2.imwrite("b_rotated.png", imageB)
      
      imageG = cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)
      imageG[:, :, 0] = 0
      imageG[:, :, 2] = 0
      cv2.imwrite("g_rotated.png", imageG)
      
      imageR = cv2.cvtColor(r,cv2.COLOR_GRAY2RGB)
      imageR[:, :, 0] = 0
      imageR[:, :, 1] = 0
      cv2.imwrite("r_rotated.png", imageR)
      
  ret,b = cv2.threshold(b,140,255,cv2.THRESH_BINARY)
  ret,g = cv2.threshold(g,140,255,cv2.THRESH_BINARY)
  ret,r = cv2.threshold(r,140,255,cv2.THRESH_BINARY)  
  
  g = matchImage(g, r)
  b = matchImage(b, r)  
  
  #rg = cv2.addWeighted(r,0.33,g,0.33,0)
  rgbI = cv2.addWeighted(cv2.addWeighted(r,0.33,g,0.33,0),0.66,b,0.33,0)
  checkImages.append(rgbI)
  
  cv2.imwrite("rgbMerged.png", rgbI)
  
  # th2 = cv2.adaptiveThreshold(rgbI,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            # cv2.THRESH_BINARY,55,15)
  # th3 = cv2.adaptiveThreshold(rgbI,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            # cv2.THRESH_BINARY,55,15)
  
  # cv2.imshow("th2", th2)
  # cv2.imshow("th3", th3)
  # # cv2.imshow("r", r)
  # # cv2.imshow("g", g)
  # # cv2.imshow("b", b)
  # cv2.waitKey(0)
  
  # checkImages.append(cv2.bitwise_or(r, g))
  # checkImages.append(cv2.bitwise_or(g, b))
  # checkImages.append(cv2.bitwise_or(b, r))
  
  # checkImages.append(cv2.bitwise_and(r, g))
  # checkImages.append(cv2.bitwise_and(g, b))
  # checkImages.append(cv2.bitwise_and(b, r))
  
  # checkImages.append(cv2.bitwise_or(r, cv2.bitwise_or(g, b)))
  # checkImages.append(cv2.bitwise_and(r, cv2.bitwise_and(g, b)))
  
  # checkImages.append(cv2.bitwise_or(r, cv2.bitwise_and(g, b)))
  # checkImages.append(cv2.bitwise_or(g, cv2.bitwise_and(b, r)))
  # checkImages.append(cv2.bitwise_or(b, cv2.bitwise_and(r, g)))
  
  # checkImages.append(cv2.bitwise_and(r, cv2.bitwise_or(g, b)))
  # checkImages.append(cv2.bitwise_and(g, cv2.bitwise_or(b, r)))
  # checkImages.append(cv2.bitwise_and(b, cv2.bitwise_or(r, g)))

  for checkImage in checkImages:      
      #cv2.imshow("test", checkImage)
      #cv2.waitKey(0)
      decodedObjects=pyzbar.decode(checkImage)
      for obj in decodedObjects: 
        if DISPLAY:
            if obj is not None:
                #countJ += 1     
                pts = obj.polygon 
                joinImageRGB = cv2.merge((b,g,r))
                joinImageRGB = cv2.cvtColor(rgbI,cv2.COLOR_GRAY2RGB)
                if pts:
                    cv2.line(image, pts[0], pts[1], [0, 0, 255], 2)
                    cv2.line(image, pts[1], pts[2], [0, 0, 255], 2)
                    cv2.line(image, pts[2], pts[3], [0, 0, 255], 2)
                    cv2.line(image, pts[3], pts[0], [0, 0, 255], 2)
                    cv2.putText(image,str(obj.data), (pts[0][0],pts[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [0, 0, 255], 2, 2)
                    rR = cv2.cvtColor(r,cv2.COLOR_GRAY2RGB)
                    rR[:, :, 0] = 0
                    rR[:, :, 1] = 0
                    cv2.imwrite("r_orig.png", rR)
                    cv2.putText(rR, "Red splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)

                    gG = cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)
                    gG[:, :, 0] = 0
                    gG[:, :, 2] = 0
                    cv2.imwrite("g_orig.png", gG)
                    cv2.putText(gG, "Green splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)

                    bB = cv2.cvtColor(b,cv2.COLOR_GRAY2RGB)
                    bB[:, :, 1] = 0
                    bB[:, :, 2] = 0
                    cv2.imwrite("b_orig.png", bB)
                    cv2.putText(bB, "Blue splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)

                    cv2.putText(joinImageRGB, "Merged Result", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 0], 2, 2)

                    #cv2.putText(image, "Detected Result on Original Image", (25,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 0], 2, 2)
                    
                    cv2.imwrite("results_final.png", joinImageRGB)
                    
                    visRG = np.concatenate((bB, gG), axis=1)
                    visBJ = np.concatenate((rR, joinImageRGB), axis=1)

                    dim = (3*width//4, 3*height//4)
                    vis = cv2.resize(np.concatenate((visRG, visBJ), axis=0), dim)
                    vis = np.concatenate((cv2.resize(image, dim), vis), axis=1)

                    #cv2.putText(vis, str(countJ)+" correct / "+str(count)+" frames = "+str(round(100*countJ/count,2))+"%", (25,35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0, 0, 0], 2, 2)
                    #cv2.putText(vis, "Percentage: "+str(round(100*countJ/count,2))+"%", (25,50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0, 0, 0], 2, 2)
                    cv2.imwrite("results.png", vis)
                    cv2.imwrite("results_image.png", image)
                    cv2.imshow("vis", vis)
                    cv2.waitKey(1)

            return obj
        else:
            return obj
  

print("python readQR.py [qr image file]")
print("[qr image file] can be either of: JPG, PNG, BMP")
print("e.g. python readQR.py qrCode.png")

if __name__ == '__main__':
    argument = "qr.png"
    if len(sys.argv) > 1:
        argument = sys.argv[1]
    setTestRandomDot(False)
    image = cv2.imread(argument)  
    obj = decodeColourQR(image)
    print(obj)





