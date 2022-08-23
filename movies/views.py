from distutils.log import info
from itertools import product
from multiprocessing import context
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import Ip, Message, Information, Product, Smmtp, User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
import cv2
import numpy as np
import requests
from smtplib import SMTP
from django.shortcuts import render

import os
import sys

def index(request):
    products = Product.objects.all()

    content = {
        "products": products
    }

    return render(request, 'index.html', content)

def hakkimizda(request):
    info = Information.objects.all()

    content = {
        "info": info
    }

    return render(request, 'index.html', content)

def hakkimizda(request):
    
    bilgi = Information.objects.all()
    content = {
        "bilgi": bilgi
    }
    return render(request, 'hakkimizda.html', content)

def kişimail(request):
    users = User.objects.all()

    content = {
        "users": users
    }
    return render(request, 'kişimail.html', content)

def kamerakayit(request):
    
 
 #urller = Ip.ip
 #for x in urller:
  #print(x)
 #url = "http://"+ urller +":8080//shot.jpg"
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
        #mesajdeneme = Message.users.all()

         
        if(format(label)==labels[17]):      
            messagex = Message.objects.all()
            for m in messagex : 
             smtpx = Smmtp.objects.all()
            for s in smtpx :

             usera = User.objects.all()
            for s in usera :
             
             try:
                # Mail Mesaj Bilgisi 
                subcjet = m.subject
                message = m.text
               # sendTo = "busecetin587@gmail.com"
                sendTo = m.Users
               # userd = User.objects.get()
                #sendTo = [val for val in Message.objects.all() if val in userd.objects.all()]
                content = "Subject: {0}\n\n{1}".format(subcjet,message)
                

                # Hesap Bilgileri 
                myMailAdress = "buseetinn@gmail.com"
                password = "zwgmhpyrfbtqnhlr"

                # Kime Gönderilecek Bilgisi
                #sendTo = m.users
                #host, port
                #mail = SMTP(s.host, s.port)
                mail = SMTP("smtp.gmail.com", 587)
                #sunucuya bağlanma
                mail.ehlo()
                #verileri şifreleme
                mail.starttls()
                #mail sunucusunda oturum açma
                mail.login(myMailAdress,password)
                #maili gönderme
                mail.sendmail(myMailAdress, sendTo, content.encode("utf-8"))
                print("Mail Gönderme İşlemi Başarılı!")
             except Exception as e:
                print("Hata Oluştu!\n {0}".format(e)) 
                

  
        label = "{}: {:.2f}%".format(label, confidence*100)
        print("predicted object {}".format(label))
 
        cv2.rectangle(frame, (x,y),(x + w,y + h),box_color,2)
        cv2.putText(frame,label,(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        
        
    cv2.imshow("Android Camera", frame) 

    if cv2.waitKey(1) == 27:
        break
 
    
 return render(request, 'kamerakayit.html')

def smtp(request):
    return render(request, 'smtp.html')

#def mail(request):
 #   messages = Message.objects.all()

  #  content = {
   #     "messages": messages
    #}
    #return render(request, 'mail.html',content)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            exam = (request, user)
            login(exam)
            return redirect("index")
        else:
            return render(request, "login.html", {
                "error": "username ya da parola yanlış"
            })

    return render(request, "login.html")


def hata(request):
    return render(request, '404.html')

def admin(request):
    return render(request, 'admin.html')

def youtube(request):
    return render(request, '_youtube.html')

def cikis(request):
    return render(request, 'cikis.html')

def admin_login(request):
    
    return render(request, 'admin_login.html')

def kayitweb(request):
    return render(request, 'kayitweb.html')
    
def sifreu(request):
    return render(request, 'forgot-password.html')

def MailSender(target,message):
 try:
                # Mail Mesaj Bilgisi 
                subcjet = Message.subject
                message = Message.text
                content = "Subject: {0}\n\n{1}".format(subcjet,message)

                # Hesap Bilgileri 
                myMailAdress = "buseetinn@gmail.com"
                password = "zwgmhpyrfbtqnhlr"

                # Kime Gönderilecek Bilgisi
                sendTo = target.get('User')

                #host, port
                mail = SMTP("smtp.gmail.com", 587)
                #sunucuya bağlanma
                mail.ehlo()
                #verileri şifreleme
                mail.starttls()
                #mail sunucusunda oturum açma
                mail.login(myMailAdress,password)
                #maili gönderme
                mail.sendmail(myMailAdress, sendTo, content.encode("utf-8"))
                print("Mail Gönderme İşlemi Başarılı!")
 except Exception as e:
                print("Hata Oluştu!\n {0}".format(e)) 
                return render(target,message, 'mail.html')


def movie_details(request, slug):
    return render(request, 'movie-details.html', {
        "slug": slug
    })