import cv2, os
import numpy as np
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt
import random
sift = cv2.SIFT_create()

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
    # FLANN_INDEX_LINEAR = 0
    # FLANN_INDEX_KDTREE = 1
    # FLANN_INDEX_KMEANS = 2
    # FLANN_INDEX_COMPOSITE = 3
    # FLANN_INDEX_KDTREE_SINGLE = 4
    # FLANN_INDEX_HIERARCHICAL = 5
    # FLANN_INDEX_LSH = 6
    # FLANN_INDEX_SAVED = 254
    # FLANN_INDEX_AUTOTUNED = 255
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
    im_out = cv2.warpPerspective(img1, M, (img2.shape[1],img2.shape[0]))
    return im_out

white = [255,255,255]
cap = cv2.VideoCapture('hard.MOV')
count = 0
countRGB = 0
countR = 0
countG = 0
countB = 0
countJ = 0
kernel = np.ones((3,3),np.uint8)
pts=[(0,0), (0,0),(0,0),(0,0)]
video = None

TEST_RANDOM_DOT = True

COVER = 20 #percentage

for i in range(100):
  image = cv2.imread("qr_Colour.png")  
  decodedObjects = []
  checkImages = []
  count += 1  
  scale_percent = 400/image.shape[1] # percent of original size
  width = int(image.shape[1] * scale_percent)
  height = int(image.shape[0] * scale_percent)  
  image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)  
  
  border = 0 #width//10 + height//10    
  emptyImg = np.zeros((height,width), dtype=np.uint8)   
  image= cv2.copyMakeBorder(image,border,border,border,border,cv2.BORDER_CONSTANT,value=white)  
  image = increase_brightness(image)
  
  # colorReduce()
  div = 32
  image = image // div * div + div // 2 
  
  if TEST_RANDOM_DOT:
    #image = cv2.circle(image, (random.randint(0,width), random.randint(0,height)), random.randint(20,100), [random.randint(0,255),random.randint(0,255),random.randint(0,255)], -1)
    image = cv2.circle(image, (random.randint(0,width), random.randint(0,height)), int(COVER*width/100), [128,128,128], -1)
  
  height, width, depth = image.shape 
  checkImages.append(image)  
  b,g,r = cv2.split(image)  
  g = cv2.rotate(g, cv2.ROTATE_90_COUNTERCLOCKWISE)
  b = cv2.rotate(b, cv2.cv2.ROTATE_90_CLOCKWISE)
  
  ret,b = cv2.threshold(b,140,255,cv2.THRESH_BINARY)
  ret,g = cv2.threshold(g,140,255,cv2.THRESH_BINARY)
  ret,r = cv2.threshold(r,140,255,cv2.THRESH_BINARY)  
  
  g = matchImage(g, r)
  b = matchImage(b, r)  
  
  checkImages.append(cv2.bitwise_or(r, g))
  checkImages.append(cv2.bitwise_or(g, b))
  checkImages.append(cv2.bitwise_or(b, r))
  
  checkImages.append(cv2.bitwise_and(r, g))
  checkImages.append(cv2.bitwise_and(g, b))
  checkImages.append(cv2.bitwise_and(b, r))
  
  checkImages.append(cv2.bitwise_or(r, cv2.bitwise_or(g, b)))
  checkImages.append(cv2.bitwise_and(r, cv2.bitwise_and(g, b)))
  
  # checkImages.append(cv2.bitwise_or(r, cv2.bitwise_and(g, b)))
  # checkImages.append(cv2.bitwise_or(g, cv2.bitwise_and(b, r)))
  # checkImages.append(cv2.bitwise_or(b, cv2.bitwise_and(r, g)))
  
  # checkImages.append(cv2.bitwise_and(r, cv2.bitwise_or(g, b)))
  # checkImages.append(cv2.bitwise_and(g, cv2.bitwise_or(b, r)))
  # checkImages.append(cv2.bitwise_and(b, cv2.bitwise_or(r, g)))

  joinImageRGB = cv2.merge((b,g,r))

  for checkImage in checkImages:      
      decodedObjects=pyzbar.decode(checkImage)
      for obj in decodedObjects:        
         countJ += 1     
         pts = obj.polygon 
         if pts:
             cv2.line(image, pts[0], pts[1], [0, 0, 255], 2)
             cv2.line(image, pts[1], pts[2], [0, 0, 255], 2)
             cv2.line(image, pts[2], pts[3], [0, 0, 255], 2)
             cv2.line(image, pts[3], pts[0], [0, 0, 255], 2)
             cv2.putText(image,str(obj.data), (pts[0][0],pts[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [0, 0, 255], 2, 2)
             #image = cv2.rectangle(image, (x,y), (x+w, y+h), [0, 0, 255], 2)
             break
      else:
         continue  # only executed if the inner loop did NOT break
      break  # only executed if the inner loop DID break

  rR = cv2.cvtColor(r,cv2.COLOR_GRAY2RGB)
  rR[:, :, 0] = 0
  rR[:, :, 1] = 0
  cv2.putText(rR, "Red splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)
  
  gG = cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)
  gG[:, :, 0] = 0
  gG[:, :, 2] = 0
  cv2.putText(gG, "Green splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)
  
  bB = cv2.cvtColor(b,cv2.COLOR_GRAY2RGB)
  bB[:, :, 1] = 0
  bB[:, :, 2] = 0
  cv2.putText(bB, "Blue splitted Channel", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)
  
  cv2.putText(joinImageRGB, "Merged Result", (width//3,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2, 2)
  
  cv2.putText(image, "Detected Result on Original Image", (25,height-25), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 0], 2, 2)
    
  visRG = np.concatenate((bB, gG), axis=1)
  visBJ = np.concatenate((rR, joinImageRGB), axis=1)
  
  dim = (3*width//4, 3*height//4)
  vis = cv2.resize(np.concatenate((visRG, visBJ), axis=0), dim)
  vis = np.concatenate((cv2.resize(image, dim), vis), axis=1)
  
  cv2.putText(vis, str(countJ)+" correct from "+str(count)+" frames", (25,35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0, 0, 0], 2, 2)
  cv2.putText(vis, "Percentage: "+str(round(100*countJ/count,2))+"%", (25,65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [0, 0, 0], 2, 2)
    
  cv2.imshow("vis", vis)
  if video is None:
      #height, width, depth = vis.shape 
      video = cv2.VideoWriter("output.avi", 0, 30, (vis.shape[1],vis.shape[0]))
      
  video.write(vis)

  if cv2.waitKey(1) == 27:                     # exit if Escape is hit
      break

cv2.waitKey(0)  
cap.release()
cv2.destroyAllWindows()
video.release()

print("count", count)
print("countJ", countJ)