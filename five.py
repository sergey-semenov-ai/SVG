#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:52:07 2020

@author: sergey
"""

import numpy as np
import cv2, time, os

from tensorflow.keras import models
#from tensorflow.keras.preprocessing import image
import pytesseract as rec


# Загрузи НС

net = models.load_model('//home/sergey/AFE/SVG/Trucks_CB.h5')

ans = ['Фон','Грузовик']

#video = cv2.VideoCapture(0)
#video = cv2.VideoCapture('rtsp://admin:admin@192.168.10.20:554/1/1')
video = cv2.VideoCapture('//home/sergey/AFE/SVG/video/2268-video.mp4')  #759
video_d = cv2.VideoCapture('//home/sergey/AFE/SVG/video/2269-video.mp4')
video.set(cv2.CAP_PROP_POS_MSEC, 4*60*1000+46*1000)


ww = video.get(cv2.CAP_PROP_FRAME_WIDTH)
hh = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

i=1
na=167

save_path = 'detected/'



def get_time (img):
    
    #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, threshold_image = cv2.threshold(gray_image, 225, 255, cv2.THRESH_BINARY_INV)
    ans = rec.image_to_string(img)
    #cv2.imwrite('temp2.jpg', threshold_image)
    
    return ans[:11]

def get_M_secs(s):
    
    try:
        hh = int(s[0:2])
        mm = int(s[3:5])
        ss = int(s[6:8])
        ms = int(s[9:11])
        
        #print (hh,mm,ss,ms)
        
        return (hh*3600+mm*60+ss)*1000 + ms
    except:
        
        return -1
    



ret, frame = video_d.read()
rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
date_img = rgb_image[0:43,215:445,:] 

ST = get_M_secs( get_time(date_img) )
    
print (ST)
print (get_time(date_img))

lastFrame = frame
video_d.release()
    
while(True):
	
		
	
    
    ret, frame = video.read()
	
        
    if ret:
		
        if (i%1 == 0):
		
            
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            date_img = rgb_image[0:43,215:445,:] 
            
            
            rgb_image = cv2.resize(rgb_image,(250,136))
		
            rgb_image = rgb_image/255

            rgb_image = np.expand_dims(rgb_image, axis = 0)
            
            pred = net.predict(rgb_image)
            
            try:
                frame = cv2.resize(frame,(853, 480))
                cv2.imshow('frame1',frame)
            except:
                pass

            
            if pred[0][0] > 0.5:
                print ('Грузовик')
               
                
                current_T = get_time(date_img)
                current = get_M_secs( current_T )
                         
                    
                print ('текущие секунды ', current) 
                # захватил текущие милисекунды 
                 
                 # считаю разницу от начала
                 
                we_start_at = current - ST 
                #if we_start_at > 10000:
                #    we_start_at = we_start_at - 500
                    
                video_d = cv2.VideoCapture('video/2269-video.mp4')     
                video_d.set(cv2.CAP_PROP_POS_MSEC, we_start_at)
                
                last_diff = we_start_at
                
                print ('стартовый сдвиг', last_diff)
                
                print ('время на первом видео ', current_T)
                ret, frame_D = video_d.read()
                rgb_image_D = cv2.cvtColor(frame_D, cv2.COLOR_BGR2RGB)
            
                date_img_D = rgb_image_D[0:43,215:445,:] 
                #date_img_D = cv2.resize(date_img_D, (480, 80))
                
                time_D = get_time(date_img_D)
                current_D = get_M_secs( time_D )
                
                if current < current_D:
                    we_start_at = we_start_at - (current_D - current) - 150
                    current_D = current_D - (current_D - current) - 150
                
                video_d.set(cv2.CAP_PROP_POS_MSEC, we_start_at)
                
                current_diff = current - current_D
                
                print ('на втором видео стартую с времени ', time_D)
                
                
                
                
                while (current_diff >= 0):
                    
                    print (last_diff, current_diff)
                    lastFrame = frame_D
                    #last_diff = current_diff
                    last_time = time_D
                    
                    ret, frame_D = video_d.read()
                    rgb_image_D = cv2.cvtColor(frame_D, cv2.COLOR_BGR2RGB)
            
                    date_img_D = rgb_image_D[0:43,215:445,:] 
                    #date_img_D = cv2.resize(date_img_D, (480, 80))
    
                    time_D = get_time(date_img_D)
                    current_D = get_M_secs( time_D )
                
                    current_diff = current - current_D
                
                    
                print (current_T)
                print (last_time)
                print (time_D)
                
                STOPFLAG = True
                lastFrame = cv2.resize(lastFrame,(853, 480))
                cv2.imshow('frame2',lastFrame)    
                    
                cv2.waitKey(4000)
                
                video_d.release()
                          
                
                
                
                
#                pics = []
#                for k in range(5):
#                    ret, frame = video.read()
#                    pics.append(frame)
            #else:
                #print ('Земля')  

        
        

    else:
        break

    inn = cv2.waitKey(1) & 0xFF	
    if inn == ord('q'):
        break
    
  

    i += 1
    
    
video.release()
cv2.destroyAllWindows()

video = cv2.VideoCapture('video/2268-video.mp4')  #759
video_d = cv2.VideoCapture('video/2269-video.mp4')
video_d.get(cv2.CAP_PROP_FRAME_COUNT)
