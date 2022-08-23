import cv2
import numpy as np
import requests
from smtplib import SMTP
from django.shortcuts import render
#from .models import Message

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horseapp.settings")
import django
django.setup()



#from horseapp.movies.models import Message

url = "http://192.168.2.253:8080//shot.jpg"


while True:
    
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    frame = cv2.resize(img, (640, 480))
    
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    
    frame_blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), swapRB=True, crop=False)

    labels = ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
         "trafficlight","firehydrant","stopsign","parkingmeter","bench","bird","cat",
         "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
         "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sportsball",
         "kite","baseballbat","baseballglove","skateboard","surfboard","tennisracket",
         "bottle","wineglass","cup","fork","knife","spoon","bowl","banana","apple",
         "sandwich","orange","broccoli","carrot","hotdog","pizza","donut","cake","chair",
         "sofa","pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse",
         "remote","keyboard","cellphone","microwave","oven","toaster","sink","refrigerator",
         "book","clock","vase","scissors","teddybear","hairdrier","toothbrush"]


    
    colors = ["0,255,255","0,0,255","255,0,0","255,255,0","0,255,0"]
    colors = [np.array(color.split(",")).astype("int") for color in colors]
    colors = np.array(colors)
    colors = np.tile(colors,(18,1))


    model = cv2.dnn.readNetFromDarknet("C:/Users/BUSE/Desktop/yolov3/yolo_pretrained_model/pretrained_model/yolov3.cfg","C:/Users/BUSE/Desktop/yolov3/yolo_pretrained_model/pretrained_model/yolov3.weights")

    layers = model.getLayerNames()
    output_layer = [layers[layer - 1] for layer in model.getUnconnectedOutLayers()]
    
    model.setInput(frame_blob)
    
    detection_layers = model.forward(output_layer)

    ids_list = []
    boxes_list = []
    confidences_list = []
        
    for detection_layer in detection_layers:
        for object_detection in detection_layer:
            
            scores = object_detection[5:]
            predicted_id = np.argmax(scores)
            confidence = scores[predicted_id]
            
            if confidence > 0.20:
                
                label = labels[predicted_id]
                bounding_box = object_detection[0:4] * np.array([frame_width,frame_height,frame_width,frame_height])
                (box_center_x, box_center_y, w, h) = bounding_box.astype("int")
                
                x = int(box_center_x - (w/2))
                y = int(box_center_y - (h/2))

                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([x, y, int(w), int(h)])
                
    max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)
 
    for max_id in max_ids:
        
        max_class_id = max_id
        box = boxes_list[max_class_id]
        
        x = box[0] 
        y = box[1] 
        w = box[2] 
        h = box[3] 
         
        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]
 
        box_color = colors[predicted_id]
        box_color = [int(each) for each in box_color]
        
       # if(format(label)==labels[17]):
       #  mail_addresses = Message.objects.all
        #for mail_addres in mail_addresses :
         #       MailSender(mail_addres)
          #      def MailSender(target,message):
        
    
            
        label = "{}: {:.2f}%".format(label, confidence*100)
        print("predicted object {}".format(label))
 
        cv2.rectangle(frame, (x,y),(x + w,y + h),box_color,2)
        cv2.putText(frame,label,(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        
        
    cv2.imshow("Android Camera", frame) 

    if cv2.waitKey(1) == 27:
        break
 
cv2.destroyAllWindows()     