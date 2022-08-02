del *.ppm
.\poppler\Library\bin\pdftoppm.exe .\temp.pdf image
copy image-01.ppm image.png
copy image-1.ppm image.png
del *.ppm
ren image.png image.ppm