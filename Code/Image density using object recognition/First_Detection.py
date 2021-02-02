from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "test.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

count=0
for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    if(eachObject["name"]=="car"):
    	count = count+1
print("count",count)