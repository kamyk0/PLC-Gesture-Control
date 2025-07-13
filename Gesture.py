import cv2
import mediapipe as mp
import numpy as np
import math
import snap7

vid = cv2.VideoCapture(0)
vid.set(3, 1280)
mphands = mp.solutions.hands
Hands = mphands.Hands(max_num_hands= 1, min_detection_confidence= 0.7, min_tracking_confidence= 0.6 )
mpdraw = mp.solutions.drawing_utils

plc =snap7.client.Client()
plc.connect('192.168.1.111',0,1)

def writeBool(bit_offset, value):
	reading = plc.db_read(db_number, start_offset_in, 1)   
	snap7.util.set_bool(reading, 0, bit_offset, value)
	plc.db_write(db_number, start_offset_in, reading)
	return None

def rectContains(rect, cx, cy):
    logic = rect[0] < cx < rect[2] and rect[1] < cy < rect[3]
    return logic

def isClosed(Tx,Ty,cx,cy):
    distance = math.sqrt((cx - Tx)**2 + (cy - Ty)**2)
    if distance > 150:
        return False
    else:
        return True




modifier_x, modifier_y = -10, -30



while True:
    _, frame = vid.read()
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = Hands.process(RGBframe)

    if result.multi_hand_landmarks:

        for handLm in result.multi_hand_landmarks :


            for id, lm in enumerate(handLm.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 0:
                    Tx, Ty = cx, cy
                if id == 4:
                    cv2.putText(frame, '1', (cx + modifier_x, cy + modifier_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 100), 6, cv2.LINE_AA)
                    Kx, Ky = cx,cy

                if id == 8:
                    cv2.putText(frame, '2', (cx + modifier_x, cy + modifier_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 100), 6, cv2.LINE_AA)
                    index = isClosed(Tx,Ty,cx,cy)
                if id == 12:
                    cv2.putText(frame, '3', (cx + modifier_x, cy + modifier_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 100), 6, cv2.LINE_AA)
                    middle = isClosed(Tx, Ty, cx, cy)
                if id == 16:
                    cv2.putText(frame, '4', (cx + modifier_x, cy + modifier_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 100), 6, cv2.LINE_AA)
                    ring = isClosed(Tx, Ty, cx, cy)
                if id == 17:
                    thumb = isClosed(Kx, Ky, cx, cy)
                if id == 20:
                    cv2.putText(frame, '5', (cx + modifier_x, cy + modifier_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 100), 6, cv2.LINE_AA)
                    pinky = isClosed(Tx, Ty, cx, cy)

        fingers = [thumb,index,middle,ring,pinky]
        if thumb:
            cv2.rectangle(frame, (200, 25), (300, 125), (255, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (200, 25), (300, 125), (0, 0, 0), cv2.FILLED)

        if index:
            cv2.rectangle(frame, (400, 25), (500, 125), (255, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (400, 25), (500, 125), (0, 0, 0), cv2.FILLED)

        if middle:
            cv2.rectangle(frame, (600, 25), (700, 125), (255, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (600, 25), (700, 125), (0, 0, 0), cv2.FILLED)

        if ring:
            cv2.rectangle(frame, (800, 25), (900, 125), (255, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (800, 25), (900, 125), (0, 0, 0), cv2.FILLED)

        if pinky:
            cv2.rectangle(frame, (1000, 25), (1100, 125), (255, 255, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (1000, 25), (1100, 125), (0, 0, 0), cv2.FILLED)

    cv2.imshow("author: Mateusz Kamyszek", frame)
    cv2.waitKey(1)
