#Ready-to-Read-Phonics-Plus = RRPP = 29181
#Ready-to-Read-Colour-Wheel = RRCW = 22576
#Junior-Journal = JJ = 22577
#School-Journal = SJ = 22578
import os
from urllib.request import urlopen

ReadingYearLevel=[1,2,3,4,5,6,7,8]

for level in ReadingYearLevel:   
    os.system("mkdir outputs\\"+str(level))
    for i in range(0, 500, 10):
        html = urlopen("https://instructionalseries.tki.org.nz/content/search/(offset)/"+str(i)+"?CurriculumLevel=all&ReadingYearLevel="+str(level)).readlines()
        #html = urlopen("https://instructionalseries.tki.org.nz/content/search/(offset)/"+str(i)+"?SearchText=&SubTreeArray[]=22577&ColourWheelLevel=all&LearningArea=all&Type=all").readlines()
        readTrue = False
        for line in html: 
            stringLine = line.decode("utf-8") 
            if "span10 resource-middle-col" in stringLine:
                readTrue = True
                continue
                
            if readTrue and stringLine.strip() != "":
                indexA = stringLine.find("href=")
                #print(stringLine.find("href="))
                indexB = stringLine.find("><h3>")
                #print(stringLine.find(".pdf"))
                stringLine = stringLine[indexA+6: indexB-1]     
                os.system("python buildFromList.py https://instructionalseries.tki.org.nz"+stringLine.strip()+" "+str(level))
                readTrue = False        
        
        
ReadingYearLevel=[29181, 22576, 22577, 22578]

for level in ReadingYearLevel:   
    os.system("mkdir outputs\\"+str(level))
    for i in range(0, 500, 10):
        html = urlopen("https://instructionalseries.tki.org.nz/content/search/(offset)/"+str(i)+"?SearchText=&SubTreeArray[]="+str(level)+"&ColourWheelLevel=all&LearningArea=all&Type=all").readlines()
        readTrue = False
        for line in html: 
            stringLine = line.decode("utf-8") 
            if "span10 resource-middle-col" in stringLine:
                readTrue = True
                continue
                
            if readTrue and stringLine.strip() != "":
                indexA = stringLine.find("href=")
                #print(stringLine.find("href="))
                indexB = stringLine.find("><h3>")
                #print(stringLine.find(".pdf"))
                stringLine = stringLine[indexA+6: indexB-1]     
                os.system("python buildFromList.py https://instructionalseries.tki.org.nz"+stringLine.strip()+" "+str(level))
                readTrue = False      