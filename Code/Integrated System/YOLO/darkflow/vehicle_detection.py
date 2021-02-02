import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 


def detection(currentGreen,tfnet,image_counter):
   fileName = "../../Test_Images/"+str(image_counter)+".jpg"
   
   img=cv2.imread(fileName,cv2.IMREAD_COLOR)
   #taking input image (colour)           
   img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   #bgr to rgb
   result=tfnet.return_predict(img)
   # print(result)
   # for car in result:
   #    label=car['label']   #extracting label
   #    print(label)
   #    if(label=="car"):    # drawing box and writing label
   #       top_left=(car['topleft']['x'],car['topleft']['y'])
   #       bottom_right=(car['bottomright']['x'],car['bottomright']['y'])
   #       img=cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)    #green box of width 5
   #       img=cv2.putText(img,label,top_left,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)   #image, label, position, font, font scale, colour: black, line width

      
   # cv2.imwrite("detection"+str(currentGreen)+".jpg",img)
  
   #plt.imshow(img)
   #plt.show()

   return result

