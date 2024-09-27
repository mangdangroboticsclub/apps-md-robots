# Facial Expression Detection

### Overview
This app enables facial expression, allowing the mini pupper to respond to user expressions. It currently recognizes two expressions: happy and sad. These gestures are detected based on the user's facial expression. A happy facial expression, prompts the pupper to display a happy face on its LCD screen and a sad facial expression displays a sad face.

### Install The Dependencies
```
cd ~/apps-md-robots/facial-expression-app/
pip install -r requirements.txt
```

### Run The App
After the App starts running, the user should frame of the camera and make either happy or sad facial expressions. This will prompt the mini pupper to display faces accordingly.
```
cd ~/apps-md-robots/facial-expression-app/
python facial_expression_app.py
```

# Advance Steps
The following steps are for further training and tuning the models. It is recommended to train the models in a personal computer instead of the pupper.

On PC, clone the repository in a desired directory and then follow the steps.

### Run collect_imgs.py
When the program starts, the user will be prompted to specify the number of classes for model training. A pop-up window will display the camera feed. The user should press 'q' to begin capturing images for the selected class. The program will take 1,000 images per class, allowing 5 seconds after every 500 images to vary the gesture angle. All parameters are adjustable within the program. It’s essential to keep both the terminal and pop-up window visible during operation to monitor progress and receive guidance.
```
git clone git@github.com:mangdangroboticsclub/apps-md-robots.git
cd apps-md-robots/facial-expression-app/train_on_PC
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
scp hand_gesture_model.p ubuntu@<IP ADDRESS OF MINI PUPPER>:~/apps-md-robots/facial-expression-app/models
```

### Testing on mini pupper
For testing, run the following code.
```
cd ~/apps-md-robots/facial-expression-app/
python facial_expression_app.py
```
