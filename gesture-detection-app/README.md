# Gesture Detection

### Overview
This app enables hand gesture detection, allowing the mini pupper to respond to user gestures. It currently recognizes four gestures: look up, look down, look left, and look right. These gestures are detected based on the direction of the user's index finger while the other fingers are curled into the palm. Pointing the index finger in any of the four directions within the camera frame will prompt the mini pupper to look accordingly.

### Install The Dependencies
```
cd ~/apps-md-robots/gesture-detection-app/
pip install -r requirements.txt
```

### Run The App
After the App starts running, the user should point the index finger within the frame of the camera. This will prompt the mini pupper to look accordingly.
```
python gesture_app.py
```

# Advance Steps
The following steps are for further training and tuning the models. It is recommended to train the models in a personal computer instead of the pupper.

On PC, clone the repository in a desired directory and then follow the steps.

### Run collect_imgs.py
When the program starts, the user will be prompted to specify the number of classes for model training. A pop-up window will display the camera feed. The user should press 'q' to begin capturing images for the selected class. The program will take 1,000 images per class, allowing 5 seconds after every 500 images to vary the gesture angle. All parameters are adjustable within the program. It’s essential to keep both the terminal and pop-up window visible during operation to monitor progress and receive guidance.
```
git clone git@github.com:mangdangroboticsclub/apps-md-robots.git
cd apps-md-robots/gesture-detection-app/train_on_PC
python collect_imgs.py
```
After image collection, a directory called ```data```should appear which should include other directories named after each class. Each of those directories should include the images collected as per class.

### Create The Dataset
This step creates the dataset just by running the ```create_dataset.py``` file.
```
python create_dataset.py
```

### Train The Model and Save
This step trains the model and saves it in a directory called ```models``` by running the ```train.py``` file. The machine learning algorithms and its parameters can be changed inside this file.
```
python train.py
```

### Copy The Model From PC to Mini Pupper
Run this code to copy the model to the Mini Pupper
```
cd models
scp hand_gesture_model.p ubuntu@<IP ADDRESS OF MINI PUPPER>:~/apps-md-robots/gesture_detection/models
```

### Testing on Mini Pupper
For testing, run the following code.

```
cd ~/apps-md-robots/gesture-detection-app/
python gesture_app.py
```
