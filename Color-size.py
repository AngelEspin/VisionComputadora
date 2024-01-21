#############################################################################################
### Asunto: Identificador de tamaño y color para sistema de clasificación de objetos      ###
### Autores: Luis Campos, Angel Espin, Isaac Leon, Erick González, Alvarado###
### Fecha: 19/12/2023                                                                     ###
#############################################################################################
import cv2
import imutils
import sys
import numpy as np
import time

referentes={'blanco':[np.array([211,211,211]),np.array([255,255,255])],'amarillo':[np.array([25,70,120]),np.array([30,255,255])], 'rojo':[np.array([139,0,0]),np.array([255,102,102])],'verde':[np.array([0,100,0]),np.array([144,238,144])]}

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]
win_name = "Camera"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

alive = True

source = cv2.VideoCapture(s)
source.set(3,640)
source.set(4,480)

tamaño="F"
color=["F","F","F"]
salida=[]
contador=0
while alive:
    has_frame, frame = source.read()
    if not has_frame:
        break
    frame = cv2.flip(frame, 1)
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    white=cv2.inRange(hsv,referentes['blanco'][0],referentes['blanco'][1])
    yellow=cv2.inRange(hsv,referentes['amarillo'][0],referentes['amarillo'][1])
    red=cv2.inRange(hsv,referentes['rojo'][0],referentes['rojo'][1])
    green=cv2.inRange(hsv,referentes['verde'][0],referentes['verde'][1])
    
    ct1=cv2.findContours(white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ct1=imutils.grab_contours(ct1)
    ct2=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ct2=imutils.grab_contours(ct2)
    ct3=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ct3=imutils.grab_contours(ct3)
    ct4=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ct4=imutils.grab_contours(ct4)
    
    contornos={'blanco':ct1,'amarillo':ct2, 'rojo':ct3, 'verde':ct4}
    
    for ama in contornos['amarillo']:
        area_amarillo=cv2.contourArea(ama)
        if(area_amarillo<=50000 and area_amarillo>10000):
            cv2.drawContours(frame, [ama],-1,(0,0,0),3)
            tamaño="T"
            color=["F","T","F"]
            
    for r in contornos['rojo']:
        area_rojo=cv2.contourArea(r)
        if(area_rojo<=50000 and area_rojo>10000):
            cv2.drawContours(frame, [r],-1,(0,0,0),3)
            tamaño="T"
            color=["T","F","F"]
    for azu in contornos['verde']:
        area_verde=cv2.contourArea(azu)
        if(area_verde<=50000 and area_verde>10000):
            cv2.drawContours(frame, [azu],-1,(0,0,0),3)
            tamaño="T"
            color=["F","F","T"]
    for b in contornos['blanco']:
        area_blanco=cv2.contourArea(b)
        if(area_blanco>50000):
            cv2.drawContours(frame, [b],-1,(0,0,0),3)
            tamaño="F"
    salida=[tamaño,color]
    
    if contador!=15:
        contador+=1
    
    cv2.imshow(win_name, frame)
    time.sleep(0.15)
    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27 or contador==15:
        contador=0
        print(salida)
        alive = False
    tamaño="F"
    color=["F","F","F"]
        
source.release()
cv2.destroyWindow(win_name)