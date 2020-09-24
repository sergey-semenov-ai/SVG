import numpy as np
import cv2, time, os

#video = cv2.VideoCapture(1)
#video1 = cv2.VideoCapture('rtsp://admin:admin@192.168.1.110:554/live/main')
#video2 = cv2.VideoCapture('rtsp://admin:admin@192.168.1.120:554/live/main')

#video1 = cv2.VideoCapture('rtsp://admin:admin@192.168.10.10:554/1/1')
#video2 = cv2.VideoCapture('rtsp://admin:admin@192.168.10.20:554/1/1')

video1 = cv2.VideoCapture('rtsp://rtsp:b312p419!@94.137.227.50:28189/axis-media/media.amp')
video2 = cv2.VideoCapture('rtsp://rtsp:b312p419!@94.137.227.50:28190/axis-media/media.amp')

video3 = cv2.VideoCapture('rtsp://rtsp:b312p419!@94.137.227.50:28187/axis-media/media.amp')
video4 = cv2.VideoCapture('rtsp://rtsp:b312p419!@94.137.227.50:28188/axis-media/media.amp')

#video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

d = ''
na = 816

path = 'temp'
while(True):
	
		
	# Capture frame-by-frame
	ret, frame1 = video1.read()
	ret, frame2 = video2.read()
	
	ret, frame3 = video3.read()
	ret, frame4 = video4.read()

	#time.sleep(0.1)
	# Display the resulting frame
        
	if ret:
		try: 
		        small1 = cv2.resize(frame1, (900,450))
		        small2 = cv2.resize(frame2, (900,450))
		        small3 = cv2.resize(frame3, (640,320))
		        small4 = cv2.resize(frame4, (640,320))
		

		        cv2.imshow('Left',small1)
		        cv2.imshow('Right',small2)
		        cv2.imshow('inDoor',small3)
		        cv2.imshow('outDoor',small4)
		except:
		        pass        
	else:
		break

	inn = cv2.waitKey(1) & 0xFF	
	if inn == ord('q'):
		break

	if inn & 0xFF == ord(' '):
		
		
		
		print('save')
		im_na_L = 'Can/waka_'+str(na)+'_'+d+'_L.jpg'
		im_na_R = 'Can/waka_'+str(na)+'_'+d+'_R.jpg'
		na = na+1
		cv2.imwrite(im_na_R, frame2)		
		cv2.imwrite(im_na_L, frame1)
		im_na_in = 'Can/road/waka_'+str(na)+'_'+d+'_in.jpg'
		im_na_out = 'Can/road/waka_'+str(na)+'_'+d+'_out.jpg'
		cv2.imwrite(im_na_in, frame3)		
		cv2.imwrite(im_na_out, frame4)
		


video1.release()
video2.release()
video3.release()
video4.release()
cv2.destroyAllWindows()

print (na)
