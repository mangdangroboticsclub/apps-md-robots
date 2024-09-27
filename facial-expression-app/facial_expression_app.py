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

import facial_expression_api
import sys
import cv2
import threading
import time

sys.path.append("..")
from api import media_api

def expression_from_face(expression):
    if expression == 'happy':
        media_api.show_image_from_path('../cartoons/Hop.jpg')
    elif expression == 'neutral':
        media_api.show_image_from_path('../cartoons/Trot.jpg')
    elif expression == 'sad':
        media_api.show_image_from_path('../cartoons/Low battery.jpg')
    else:
        media_api.show_image_from_path('../cartoons/Rest (waiting).jpg')

def main():
    model = facial_expression_api.get_model()
    cap = cv2.VideoCapture(0)
    
    while True:
        start_time = time.time()
        
        ret, frame = cap.read()
        frame = cv2.resize(frame, (320, 240))
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        expression = facial_expression_api.get_facial_expression(frame_rgb, model)
        
        if expression == "":
            cap.release()
            cv2.destroyAllWindows()
            cap = cv2.VideoCapture(0)
            break
        else:
            expression_from_face(expression)
            
        # Control frame rate
        elapsed_time = time.time() - start_time
        wait_time = max(1, int((1 / 10 - elapsed_time) * 1000))
        cv2.waitKey(wait_time)

if __name__ == '__main__':
    main()