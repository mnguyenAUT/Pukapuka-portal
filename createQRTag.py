import qrcode, sys
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

data = "E Ihowā Atua, O ngā iwi mātou rā, Āta whakarangona, Me aroha noa, Kia hua ko te pai, Kia tau tō atawhai, Manaakitia mai, Aotearoa."
if len(sys.argv) > 1:
	data = sys.argv[1]
qr = qrcode.QRCode(version = 5, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size = 1, border = 1)
qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill = "black" , back_color = "white")
img.save("qrSmall.png")

qrSmallImage = cv2.imread("qrSmall.png", 0)
smallWidth = qrSmallImage.shape[1]
smallHeight = qrSmallImage.shape[0]

colourImage = cv2.imread("image.ppm")

#colourImage=cv2.transpose(colourImage)
#colourImage=cv2.flip(colourImage,flipCode=0)
#colourImage=cv2.transpose(colourImage)
#colourImage=cv2.flip(colourImage,flipCode=0)
#colourImage=cv2.transpose(colourImage)
#colourImage=cv2.flip(colourImage,flipCode=0)

colourImage=cv2.transpose(colourImage)
colourImage=cv2.flip(colourImage,flipCode=0)
colourImage=cv2.transpose(colourImage)
colourImage=cv2.flip(colourImage,flipCode=0)

colourImageWidth = colourImage.shape[1]
#print(colourImageWidth)
#print(smallWidth)

SIZE = 7#int(colourImageWidth/(2*smallWidth))
#print(SIZE)

HALF_SIZE = int(SIZE/2)
BIG_DOT = 6
#DOT_SIZE = 3

qrSmallImage[1:9, 1:9] = qrSmallImage[1:9, 1:9] + 2
qrSmallImage[0, 8] = qrSmallImage[0, 8] + 3
qrSmallImage[8, 0] = qrSmallImage[8, 0] + 3
qrSmallImage[8, 8] = qrSmallImage[8, 8] + 3
qrSmallImage[0:1, :] = qrSmallImage[0:1, :] + 2
qrSmallImage[0:1, 9:smallWidth-9] = qrSmallImage[0:1, 9:smallWidth-9] - 3

qrSmallImage=cv2.transpose(qrSmallImage)
qrSmallImage=cv2.flip(qrSmallImage,flipCode=0)
qrSmallImage[1:9, 1:9] = qrSmallImage[1:9, 1:9] + 2
qrSmallImage[0, 8] = qrSmallImage[0, 8] + 3
qrSmallImage[8, 0] = qrSmallImage[8, 0] + 3
qrSmallImage[8, 8] = qrSmallImage[8, 8] + 3
qrSmallImage[0:1, :] = qrSmallImage[0:1, :] + 2
qrSmallImage[0:1, 9:smallWidth-9] = qrSmallImage[0:1, 9:smallWidth-9] - 3

qrSmallImage=cv2.transpose(qrSmallImage)
qrSmallImage=cv2.flip(qrSmallImage,flipCode=0)
qrSmallImage[0:1, :] = qrSmallImage[0:1, :] + 2
qrSmallImage[0:1, 0:smallWidth-9] = qrSmallImage[0:1, 0:smallWidth-9] - 3
qrSmallImage[0:smallWidth-9,0:1] = qrSmallImage[0:smallWidth-9,0:1] - 3

qrSmallImage=cv2.transpose(qrSmallImage)
qrSmallImage=cv2.flip(qrSmallImage,flipCode=0)
qrSmallImage[1:9, 1:9] = qrSmallImage[1:9, 1:9] + 2
qrSmallImage[0, 8] = qrSmallImage[0, 8] + 3
qrSmallImage[8, 0] = qrSmallImage[8, 0] + 3
qrSmallImage[8, 8] = qrSmallImage[8, 8] + 3
qrSmallImage[0:1, :] = qrSmallImage[0:1, :] + 2
qrSmallImage[0:1, 9:smallWidth-9] = qrSmallImage[0:1, 9:smallWidth-9] - 3



qrSmallImage=cv2.transpose(qrSmallImage)
qrSmallImage=cv2.flip(qrSmallImage,flipCode=0)

qrSmallImage = qrSmallImage - 2

#Process image pixel by pixel
for h in range(0, smallHeight):
	for w in range(0, smallWidth):
		#circulate = (BIG_DOT - BIG_DOT * ((h+1)*(h+1)+(w+1)*(w+1))/(smallWidth*smallWidth+smallHeight*smallHeight))
		DOT_SIZE = round(BIG_DOT/2)
		#if circulate < 1.1:
		#	break
		if qrSmallImage[h, w] == 0:			
			colourImage = cv2.rectangle(colourImage, (h*SIZE, w*SIZE), ((h+1)*SIZE, (w+1)*SIZE), (0,0,0), -1)
		elif qrSmallImage[h, w] == 255:			
			colourImage = cv2.rectangle(colourImage, (h*SIZE, w*SIZE), ((h+1)*SIZE, (w+1)*SIZE), (255,255,255), -1)
		elif qrSmallImage[h, w] == 253:
			colourImage = cv2.rectangle(colourImage, (h*SIZE+HALF_SIZE, w*SIZE+HALF_SIZE), (h*SIZE+HALF_SIZE+DOT_SIZE, w*SIZE+HALF_SIZE+DOT_SIZE), (255,255,255), -1)
		elif qrSmallImage[h, w] == 254:
			colourImage = cv2.rectangle(colourImage, (h*SIZE+HALF_SIZE, w*SIZE+HALF_SIZE), (h*SIZE+HALF_SIZE+DOT_SIZE, w*SIZE+HALF_SIZE+DOT_SIZE), (0,0,0), -1)

colourImage=cv2.transpose(colourImage)
colourImage=cv2.flip(colourImage,flipCode=0)
colourImage=cv2.transpose(colourImage)
colourImage=cv2.flip(colourImage,flipCode=0)
#cv2.imshow("colourImage", colourImage)
#colourImage = cv2.medianBlur(colourImage,3)
#colourImage = cv2.bilateralFilter(colourImage, 5, 10, 10)
cv2.imwrite("finalQR.png", colourImage)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

