import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 

options={
   'model':'./cfg/yolo.cfg',     #specifying the path of model
   'load':'./bin/yolov2.weights',   #weights
   'threshold':0.3     #minimum confidence factor to create a box, greater than 0.3 good
}

tfnet=TFNet(options)    #READ ABOUT TFNET

def detection(currentGreen,tfnet):
   fileName = "../../Test_Images/"+str((currentGreen+1))+".jpg"
   
   img=cv2.imread(fileName,cv2.IMREAD_COLOR)
   #taking input image (colour)           
   img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   #bgr to rgb
   result=tfnet.return_predict(img)
   print(result)
   for car in result:
      label=car['label']   #extracting label
      print(label)
      if(label=="car" or label=="bus" or label=="bike"):    # drawing box and writing label
         top_left=(car['topleft']['x'],car['topleft']['y'])
         bottom_right=(car['bottomright']['x'],car['bottomright']['y'])
         img=cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)    #green box of width 5
         img=cv2.putText(img,label,top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)   #image, label, position, font, font scale, colour: black, line width

      
   cv2.imwrite("detection"+str((currentGreen+1))+".jpg",img)
  
   # plt.imshow(img)
   # plt.show()

   return result

for i in range(1,4):
   detection(i,tfnet)

