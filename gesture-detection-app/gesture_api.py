#
# Copyright 2024 MangDang (www.mangdang.net)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Description: This script is designed to detect hand gesture using the trained AI model along with mediapipe.
#
# Test Method: Type "gesture" and press enter. Make different hand gestures with ONLY one hand (point up, down,
#              left, and right with your index finger, gesture to come towards you, gesture to stop with palm
#              facing the camera) to make the pupper look into different directions or move.
#

import pickle
import cv2
import mediapipe as mp
import numpy as np
import sys
import time
import threading

sys.path.append("..")
from api import move_api
from MangDang.LCD.ST7789 import ST7789

labels_dict = {0: 'come', 1: 'stop', 2: 'look up', 3: 'look down', 4: 'look right', 5: 'look left', 6: 'quit'}

# Initialize MediaPipe settings
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Setting static_image_mode to False for real-time detection
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def get_model():
    model_dict = pickle.load(open('models/hand_gesture_model.p', 'rb'))
    model = model_dict['model']

    return model

def get_gesture(frame, model):
    global mp_hands, mp_drawing, mp_drawing_styles, hands

    data_aux = []
    x_ = []
    y_ = []

    results = hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        prediction = model.predict([np.asarray(data_aux)])
        PREDICTED_GESTURE = labels_dict[int(prediction[0])]

        print(PREDICTED_GESTURE)
        return PREDICTED_GESTURE, x_, y_
    else:
        return "", "", ""

def main():
    model = get_model()
    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input == "exit":
            break
        elif user_input == "gesture":
            count = 0
            cap = cv2.VideoCapture(0)
            while True:
                start_time = time.time()

                ret, frame = cap.read()
                frame = cv2.resize(frame, (320, 240))
                H, W, _ = frame.shape
                # Flip the frame
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                gesture, x_, y_ = get_gesture(frame_rgb, model)

                if gesture == "" or x_ == "" or y_ == "":
                    pass
                else:
                    if gesture == "quit":
                        count += 1
                        if count == 3:
                            cap.release()
                            cv2.destroyAllWindows()
                            break
                    print(gesture)

                # Control frame rate
                elapsed_time = time.time() - start_time
                wait_time = max(1, int((1 / 10 - elapsed_time) * 1000))
                cv2.waitKey(wait_time)

if __name__ == '__main__':
    main()
