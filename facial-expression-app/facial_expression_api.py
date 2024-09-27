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
# Description: This script is designed to detect facial expression using the trained AI model along with mediapipe.
#
# Test Method: Type "gesture" and press enter. Look at the camera and make sad or happy face and watch the LCD showing your facial expression
#

import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import sys

sys.path.append("..")
from api import media_api

labels_dict = ['happy', 'neutral', 'sad', 'surprise']

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Setting static_image_mode to False for real-time detection
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.3)

def get_model():
    # Load the trained model
    model_dict = pickle.load(open('models/facial_expression_model.p', 'rb'))
    model = model_dict['model']
    
    return model

def get_facial_expression(frame, model):
    global mp_face_mesh, mp_drawing, mp_drawing_styles, face_mesh
    
    results = face_mesh.process(frame)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            landmark_data = []
            for landmark in landmarks.landmark:
                x = landmark.x
                y = landmark.y
                landmark_data.extend([x, y, landmark.z])

            # Predict the expression
            prediction = model.predict([np.asarray(landmark_data)])
            predicted_expression = labels_dict[int(prediction[0])]
            confidence = np.max(model.predict_proba([np.asarray(landmark_data)]))

            # Draw the face mesh
            mp_drawing.draw_landmarks(
                frame,
                landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())

        print(predicted_expression)
        return predicted_expression
    else:
        return ""

def main():
    model = get_model()
    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input == "exit":
            break
        elif user_input == "face":
            cap = cv2.VideoCapture(0)
            while True:
                start_time = time.time()
                ret, frame = cap.read()
                frame = cv2.resize(frame, (320, 240))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                expression = get_facial_expression(frame_rgb, model)
                if expression == "":
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    print(expression)
                
                # Control frame rate
                elapsed_time = time.time() - start_time
                wait_time = max(1, int((1 / 10 - elapsed_time) * 1000))
                cv2.waitKey(wait_time)

if __name__ == '__main__':
    main()