import time
import pyautogui
import cv2
import autopy
import numpy as np
import mediapipe as mp
import PoseEstimationModule as pem
from pynput.keyboard import Key,Controller
cap=cv2.VideoCapture(0)
detector=pem.poseDetector()
keyboard=Controller()
# delayCounter=0
counter=0
smoothening=40
plocX,plocY=0,0
clocX,clocY=0,  0
frameR=100#Frame Reduction
wScr,hScr=autopy.screen.size()
counter=0
while True:
    success,img=cap.read()
    img=cv2.resize(img,(900,650))
    img=cv2.flip(img,1)
    hCam, wCam, _ = img.shape
    detector.findPose(img,draw=False)
    lmList=detector.getPosition(img,draw=False)
    if lmList:
        p1,p2=lmList[1][1:],lmList[23][1:]
        left,right=lmList[18][1:],lmList[19][1:]
        shoulder=lmList[12][1:]
        l, _, _ = detector.findDistance(p1, p2)
        l1, _, _ = detector.findDistance(left, right)
        # print(p1[1],l1)
        # print(left[0],right[0])
        if right[1]<shoulder[1]:
            x1,y1=left
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            cLocX = plocX + (x3 - plocX) / smoothening
            cLocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(cLocX, cLocY)
            # cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = cLocX, cLocY
        flag=0
        if counter==0:
            if left[0]<150 and right[0]>750:
                keyboard.press(Key.space)
                flag=1
            if l1<80:
                pyautogui.click()
            if left[1]<100:
                pyautogui.click(button="right")
            if p1[1]<100:
                    keyboard.press(Key.up)
                    flag=1
            if p1[1]> 250:
                    keyboard.press(Key.down)
                    flag=1
            if left[0]<150:
                   keyboard.press(Key.left)
                   flag=1
            if right[0]>750:
                    keyboard.press(Key.right)
                    flag=1
        if flag== 1:
            keyboard.release(Key.up)
            keyboard.release(Key.down)
            keyboard.release(Key.left)
            keyboard.release(Key.right)
            keyboard.release(Key.space)
        counter+=1
    if counter==2:
        counter=0
    cv2.imshow("Hammer 2",img)
    cv2.waitKey(1)