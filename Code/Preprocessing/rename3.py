import os
os.chdir('/Users/rutwijdaptardar/Desktop/gaadi')
i=1408
for file in os.listdir():
     src=file
     dst=str(i)+".jpg"
     os.rename(src,dst)
     i+=1