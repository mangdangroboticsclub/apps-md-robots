#
# Description: This script is designed to create dataset from the collected images to train AI model for gesture detection
# 
# References: https://github.com/computervisioneng/sign-language-detector-python
#                                             

import os
import pickle
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

def gather_landmark_data(directory):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
    
    landmark_data = {}
    
    for class_name in os.listdir(directory):
        class_path = os.path.join(directory, class_name)
        if not os.path.isdir(class_path):
            continue
        for filename in os.listdir(class_path):
            if filename == '.DS_Store':
                continue
            img_path = os.path.join(class_path, filename)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Error reading {img_path}. Skipping...")
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(img_rgb)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                coords = []
                for landmark in landmarks.landmark:
                    coords.append((landmark.x, landmark.y, landmark.z))
                landmark_data[img_path] = coords
            else:
                print(f"No face detected in {img_path}. Skipping...")
    
    face_mesh.close()
    return landmark_data

def save_landmark_data(landmark_data, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(landmark_data, f)

directory = './data/'

landmark_data = gather_landmark_data(directory)

output_filepath = 'data.pickle'
save_landmark_data(landmark_data, output_filepath)
