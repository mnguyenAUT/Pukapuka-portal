from urllib.request import urlopen
html = urlopen("https://instructionalseries.tki.org.nz/Instructional-Series/Ready-to-Read-Phonics-Plus/Weka-Helps-Out").readlines()
for line in html: 
    stringLine = line.decode("utf-8") 
    if ".pdf" in stringLine and "pdf-ico" in stringLine:
        #print(stringLine)
        indexA = stringLine.find("href=")
        #print(stringLine.find("href="))
        indexB = stringLine.find(".pdf")
        #print(stringLine.find(".pdf"))
        print(stringLine[indexA+6: indexB+4])
        
        
