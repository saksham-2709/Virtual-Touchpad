# import cv2
# import time, math, numpy as np
# import HandTrackingModule as htm
# import pyautogui
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
# cap.set(3, wCam)
# cap.set(4, hCam)
# pTime = 0

# detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volRange = volume.GetVolumeRange()

# minVol = -63
# maxVol = volRange[1]
# hmin = 50
# hmax = 200
# volBar = 400
# volPer = 0
# vol = 0
# color = (0, 215, 255)

# tipIds = [4, 8, 12, 16, 20]
# mode = ''
# active = 0

# pyautogui.FAILSAFE = False
# prev_x= None
# while True:
#     success, img = cap.read()
#     flipped_frame = cv2.flip(img,1)
#     flipped_frame = detector.findHands(flipped_frame)

#     lmList = detector.findPosition(flipped_frame, draw=False)
#     fingers = []

#     if len(lmList) != 0:
#         if lmList[tipIds[0]][1] > lmList[tipIds[0 - 1]][1]:
#             fingers.append(1 if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1] else 0)
#         else:
#             fingers.append(1 if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1] else 0)

#         for id in range(1, 5):
#             fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

#         if (fingers == [0, 0, 0, 0, 0]) and (active == 0):
#             mode = 'N'
#         elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and (active == 0):
#             mode = 'Scroll'
#             active = 1
#         elif fingers == [1, 1, 0, 0, 0] and (active == 0):
#             mode = 'Volume'
#             active = 1
#         elif fingers == [1, 1, 1, 1, 1] and (active == 0):
#             mode = 'Cursor'
#             active = 1
#         elif fingers == [0, 0, 0, 0, 1] and (active == 0):
#             mode = 'TabSwitch'
#             active = 1
#         elif fingers == [0, 0, 1, 0, 0] and (active == 0):
#             mode = 'Exit'

#     if mode == 'Scroll':
#         active = 1
#         if len(lmList) != 0:
#             if fingers == [0, 1, 0, 0, 0]:
#                 pyautogui.scroll(200)
#             if fingers == [0, 1, 1, 0, 0]:
#                 pyautogui.scroll(-200)
#             elif fingers == [0, 0, 0, 0, 0]:
#                 active = 0
#                 mode = 'N'
#     if mode == 'Exit':
#         break
#     if mode == 'Volume':
#         active = 1
#         if len(lmList) != 0:
#             if fingers[-1] == 1:
#                 active = 0
#                 mode = 'N'
#             else:
#                 x1, y1 = lmList[4][1], lmList[4][2]
#                 x2, y2 = lmList[8][1], lmList[8][2]
#                 length = math.hypot(x2 - x1, y2 - y1)
#                 vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
#                 volume.SetMasterVolumeLevel(vol, None)

#     if mode == 'Cursor':
#         active = 1
#         if fingers[1:] == [0, 0, 0, 0]:
#             active = 0
#             mode = 'N'
#         else:
#             if len(lmList) != 0:
#                 x1, y1 = lmList[8][1], lmList[8][2]
#                 screen_w, screen_h = pyautogui.size()
#                 X = int(np.interp(x1, [110, 620], [0, screen_w - 1]))
#                 Y = int(np.interp(y1, [20, 350], [0, screen_h - 1]))
#                 pyautogui.moveTo(X, Y)
#                 if fingers[0] == 0:
#                     pyautogui.click()
#                 elif fingers [2]==0 and fingers[3]==0:
#                     pyautogui.click(clicks=2)
                
#     movement_threshold = 100
#     if mode == 'TabSwitch':
#       active = 1
#       if len(lmList) != 0:
#          x1 = lmList[12][1]  

#          if prev_x is None: 
#             prev_x = x1

#          movement = abs(x1 - prev_x)  

#          if movement > movement_threshold:  
#             pyautogui.hotkey('win', 'tab')
#             prev_x = None  
#             time.sleep(1)  

#         # **Exit mode if three-finger gesture is not detected**
#          if fingers != [0, 0, 0, 0, 1]:  
#             active = 0
#             mode = 'N'
#             prev_x = None

        

#     # cv2.imshow('Hand Tracking', flipped_frame)
#     cTime = time.time()
#     fps = 1 / ((cTime + 0.01) - pTime)
#     pTime = cTime

#     cv2.putText(flipped_frame, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
#     cv2.imshow('Hand LiveFeed', flipped_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


import cv2
import time, math, numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = -63
maxVol = volRange[1]
hmin = 50
hmax = 200
volBar = 400
volPer = 0
vol = 0
color = (0, 215, 255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0
mouse = Controller()
keyboard = KeyboardController()
screen_w, screen_h = pyautogui.size()
prev_x= None
while True:
    success, img = cap.read()
    flipped_frame = cv2.flip(img,1)
    flipped_frame = detector.findHands(flipped_frame)

    lmList = detector.findPosition(flipped_frame, draw=False)
    fingers = []

    if len(lmList) != 0:
        if lmList[tipIds[0]][1] > lmList[tipIds[0 - 1]][1]:
            fingers.append(1 if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1] else 0)
        else:
            fingers.append(1 if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1] else 0)

        for id in range(1, 5):
            fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

        if (fingers == [0, 0, 0, 0, 0]) and (active == 0):
            mode = 'N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and (active == 0):
            mode = 'Scroll'
            active = 1
        elif fingers == [1, 1, 0, 0, 0] and (active == 0):
            mode = 'Volume'
            active = 1
        elif fingers == [1, 1, 1, 1, 1] and (active == 0):
            mode = 'Cursor'
            active = 1
        elif fingers == [0, 0, 0, 0, 1] and (active == 0):
            mode = 'TabSwitch'
            active = 1
        elif fingers == [0, 0, 1, 0, 0] and (active == 0):
            mode = 'ex'

    if mode == 'Scroll':
        active = 1
        if len(lmList) != 0:
            if fingers == [0, 1, 0, 0, 0]:
                mouse.scroll(0, 0.5)

            if fingers == [0, 1, 1, 0, 0]:
                mouse.scroll(0, -0.5)
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'
    if mode == 'ex':
        break
    if mode == 'Volume':
        active = 1
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
            else:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                length = math.hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)

    if mode == 'Cursor':
            active = 1
            if fingers[1:] == [0, 0, 0, 0]:
                active = 0
                mode = 'N'
            else:
                if len(lmList) != 0:
                    x1, y1 = lmList[8][1], lmList[8][2]
                    X = int(np.interp(x1, [110, 620], [0, screen_w - 1]))
                    Y = int(np.interp(y1, [20, 350], [0, screen_h - 1]))
                    mouse.position = (X, Y)
                    if fingers[0] == 0:
                        mouse.click(Button.left, 1)
                    elif fingers[2] == 0 and fingers[3] == 0:
                        mouse.click(Button.left, 2)
                    
    movement_threshold = 100
    if mode == 'TabSwitch':
      active = 1
      if len(lmList) != 0:
         x1 = lmList[20][1]  
         if prev_x is None: 
            prev_x = x1
         movement = abs(x1 - prev_x)  
         if movement > movement_threshold:  
            keyboard.press(Key.cmd)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.release(Key.cmd)
            prev_x = None  
            time.sleep(1)  

         if fingers != [0, 0, 0, 0, 1]:  
            active = 0
            mode = 'N'
            prev_x = None

    cTime = time.time()
    fps = 1 / ((cTime + 0.01) - pTime)
    pTime = cTime

    cv2.putText(flipped_frame, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
    cv2.imshow('Hand LiveFeed', flipped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

