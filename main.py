#!/usr/bin/env python3
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
keysText = [["A","Z","E","R","T","Y","U","I","O","P"],["Q","S","D","F","G","H","J","K","L","M"],["W","X","C","V","B","N"]]
buttonList = []
class Key():
    def __init__(self,pos,text,size=52):
        self.pos = pos
        self.text = text
        self.size = size
    


y = 50
for row in keysText:
    l = []
    pos1 = 15
    for text in row:
        if text=="W":
            pos1+=55
        l.append(Key((pos1,y),text))
        pos1+=55
    y+=60
    buttonList.append(l)
def drawAll(img,list):
    for row in list:
        for key in row:
            pos,size,text = key.pos,key.size,key.text
            cv2.rectangle(img,pos,(pos[0] +size,pos[1]+size),(255,0,255),cv2.FILLED)
            cv2.putText(img,text,(pos[0]+5,pos[1]+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
    return img
pressedKeys = []
keyboard = Controller()
while 1:
    ret,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img,buttonList)
    if len(lmList) !=0 :
        for row in buttonList:
            for key in row:
                x,y = key.pos
                w = h = key.size
                if x < lmList[8][0] < x+w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img,(x,y),(x +w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                    l = detector.findDistance(8,12,img,draw=False)[0]
                    l2 = detector.findDistance(8,16,img,draw=False)[0]
                    if l < 30 and l2>45:
                        try:
                            if pressedKeys[-1] != key.text:
                                cv2.rectangle(img,(x,y),(x + w,y+h),(0,0,255),cv2.FILLED)
                                cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                pressedKeys.append(key.text)
                                print(pressedKeys)
                        except IndexError:
                            cv2.rectangle(img,(x,y),(x + w,y+h),(0,0,255),cv2.FILLED)
                            cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                            pressedKeys.append(key.text)
                            print(pressedKeys)
                    elif l2<45:
                        
                        try :
                            if (pressedKeys[-1] == pressedKeys[-2] and pressedKeys[-1] == key.text):
                                pass
                            elif (pressedKeys[-1] == key.text):
                                cv2.rectangle(img,(x,y),(x +w,y+h),(0,0,255),cv2.FILLED)
                                cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                pressedKeys.append(key.text)                         
                            else :
                                cv2.rectangle(img,(x,y),(x +w,y+h),(0,0,255),cv2.FILLED)
                                cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                                pressedKeys.append(key.text)
                                pressedKeys.append(key.text)
                                print(pressedKeys)
                                #keyboard.press(key.text)
                                #keyboard.release(key.text)
                        except IndexError:
                            cv2.rectangle(img,(x,y),(x +w,y+h),(0,0,255),cv2.FILLED)
                            cv2.putText(img,key.text,(x+5,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),3)
                            pressedKeys.append(key.text)
                            print(pressedKeys)
                            #keyboard.press(key.text) Working on windows brk
                            #keyboard.release(key.text)

                        
                        sleep(0.15)
    
    cv2.imshow("Camera",img)
    cv2.waitKey(1)