#Ready-to-Read-Phonics-Plus = RRPP = 29181
#Ready-to-Read-Colour-Wheel = RRCW = 22576
#Junior Journal = JJ = 22577
#School Journal = SJ = 22578

import cv2
import requests, os, sys
import PySimpleGUI as sg
from PIL import Image
import time

# Resize PNG file to size (300, 300)
size = (700, 800)
im = cv2.imread("finalQR.png")
im = cv2.resize(im, size)
cv2.imwrite("temp.png", im)

layout = [
[sg.Text("Pukapuka portal - QR Book from TKI (instructionalseries.tki.org.nz) - made by Minh.Nguyen@Aut.Ac.Nz")], 
[sg.Text("URL from tki.org.nz:"),
sg.In(size=(68, 1), enable_events=True, key="URL-Value"),
sg.Button("GENERATE")
],
[sg.Image("temp.png", key='-IMAGE-')]
]

# Create the window
window = sg.Window("Pukapuka portal - QR Book from TKI (instructionalseries.tki.org.nz) - made by Minh.Nguyen@Aut.Ac.Nz", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    elif event == "GENERATE":        
        window['-IMAGE-'].update("wait.png")
        window.refresh()
        #sg.Popup('Working now, please wait...', title='Poup')
        urlValue = values["URL-Value"]
        urlValue_short = urlValue.replace("https://instructionalseries.tki.org.nz/Instructional-Series/", "")
        urlValue_short = urlValue_short.replace("Ready-to-Read-Phonics-Plus", "RRPP")
        urlValue_short = urlValue_short.replace("Ready-to-Read-Colour-Wheel", "RRCW")
        urlValue_short = urlValue_short.replace("Junior-Journal", "JJ")
        urlValue_short = urlValue_short.replace("School-Journal", "SJ")
        splitted = urlValue.split("/")
        #print(splitted)
        #pdfValue = values["URL-Pdf"]
        os.system("python pdf2Image.py \""+str(urlValue)+"\"")
        #os.system("python createQRTag.py \"https://cerv.aut.ac.nz/tki/?url="+str(urlValue)+"\"")
        os.system("python createQRTag.py \"cerv.aut.ac.nz/tki/?u="+str(urlValue_short)+"\"")
        #update page
        im = cv2.imread("finalQR.png")
        if splitted[-1] != "":
            cv2.imwrite("outputs/"+splitted[-1]+".png", im)
        
        im = cv2.resize(im, size)
        cv2.imwrite("temp.png", im)
        window['-IMAGE-'].update("temp.png")
        
window.close()