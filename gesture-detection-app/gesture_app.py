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

import gesture_api
import sys
import cv2
import threading
import time

sys.path.append("..")
from api import move_api
from MangDang.LCD.ST7789 import ST7789

def gesture_look_up(gesture, gestures_dict):
    start_msg = {**move_api._MSG, "ry": 1.0}
    # start_msg, stop_msg = gestures_dict[gesture]()

    move_api.send_msgs([start_msg])

def gesture_look_down(gesture, gestures_dict):
    start_msg = {**move_api._MSG, "ry": -1.0}
    # start_msg, stop_msg = gestures_dict[gesture]()

    move_api.send_msgs([start_msg])

def gesture_look_left(gesture, gestures_dict):
    start_msg = {**move_api._MSG, "rx": 1.0}
    # start_msg, stop_msg = gestures_dict[gesture]()

    move_api.send_msgs([start_msg])

def gesture_look_right(gesture, gestures_dict):
    start_msg = {**move_api._MSG, "rx": -1.0}
    # start_msg, stop_msg = gestures_dict[gesture]()

    move_api.send_msgs([start_msg])

gestures_dict = {'come': move_api.move_forward, 'stop': move_api.move_forward, 'look up': gesture_look_up,
                 'look right': gesture_look_right, 'look left': gesture_look_left, 'look down': gesture_look_down}

def movement_from_gesture(cap, gesture):
    if gesture == 'quit':
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
    elif gesture == "look up":
        gesture_thread = threading.Thread(target=gesture_look_up, args=[gesture, gestures_dict])
        gesture_thread.start()
    elif gesture == "look down":
        gesture_thread = threading.Thread(target=gesture_look_down, args=[gesture, gestures_dict])
        gesture_thread.start()
    elif gesture == "look left":
        gesture_thread = threading.Thread(target=gesture_look_left, args=[gesture, gestures_dict])
        gesture_thread.start()
    elif gesture == "look right":
        gesture_thread = threading.Thread(target=gesture_look_right, args=[gesture, gestures_dict])
        gesture_thread.start()

def main():
    model = gesture_api.get_model()
    count = 0
    cap = cv2.VideoCapture(0)
    disp = ST7789()
    disp.begin()
    
    while True:
        start_time = time.time()

        ret, frame = cap.read()
        frame = cv2.resize(frame, (320, 240))
        H, W, _ = frame.shape
        # Flip the frame
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        gesture, x_, y_ = gesture_api.get_gesture(frame_rgb, model)

        if gesture == "" or x_ == "" or y_ == "":
            pass
        else:
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 0, 0), 2)
            cv2.putText(frame_rgb, gesture, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            disp.display(frame_rgb)

            if gesture == "quit":
                count += 1
                if count == 3:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            else:
                count = 0
                movement_from_gesture(cap, gesture)

        # Control frame rate
        elapsed_time = time.time() - start_time
        wait_time = max(1, int((1 / 10 - elapsed_time) * 1000))
        cv2.waitKey(wait_time)

if __name__ == '__main__':
    main()
