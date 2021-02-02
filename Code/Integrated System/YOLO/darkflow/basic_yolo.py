import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 

options={
   'model':'./cfg/yolo.cfg',
   'load':'./bin/yolov2.weights',
   'threshold':0.3
}

tfnet=TFNet(options)
img=cv2.imread("../../Test_Images/iter_1.4.jpg",cv2.IMREAD_COLOR)              
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result=tfnet.return_predict(img)
print(result)

for car in result:
   label=car['label']
   print(label)
   if(label=="car" or label=="truck"):
      top_left=(car['topleft']['x'],car['topleft']['y'])
      bottom_right=(car['bottomright']['x'],car['bottomright']['y'])
      img=cv2.rectangle(img,top_left,bottom_right,(0,255,0),7)
      img=cv2.putText(img,label,top_left,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)

plt.imshow(img)
plt.show()


