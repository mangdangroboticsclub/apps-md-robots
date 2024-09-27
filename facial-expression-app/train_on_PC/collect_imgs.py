#
# Description: This script is designed to collect images for creating a dataset to train AI model for gesture detection
# 
# References: https://github.com/computervisioneng/sign-language-detector-python
#      

import os
import time
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = int(input("Enter the number of classes: "))
dataset_size = 1000
variation_interval = 500  # Number of images after which to vary hand gesture

cap = cv2.VideoCapture(0)

for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print('Collecting data for class {}'.format(j))

    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        if counter % variation_interval == 0 and counter != 0:
            print(f'Collected {counter} images. Please vary your hand gesture. You have 5 seconds...')
            for i in range(5, 0, -1):
                print(i)
                time.sleep(1)
        
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(class_dir, '{}.jpg'.format(counter)), frame)

        counter += 1

cap.release()
cv2.destroyAllWindows()