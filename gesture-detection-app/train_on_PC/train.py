#
# Description: This script is designed to train AI model for gesture detection

#      

import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# Load data
data_dict = pickle.load(open('./data.pickle', 'rb'))
data = data_dict['data']
labels = data_dict['labels']

# Ensure all data samples have the same length
max_length = max(len(sample) for sample in data)
data = [np.pad(sample, (0, max_length - len(sample))) for sample in data]

# Convert to NumPy arrays
data = np.array(data)
labels = np.array(labels).astype(int)  # Convert labels to integers

# Split the dataset
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.15, shuffle=True, stratify=labels)

# Train the model
model = XGBClassifier(use_label_encoder=False)
model.fit(x_train, y_train)

# Make predictions and calculate accuracy
y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly!'.format(score * 100))

# Save the model
with open('../models/model.p', 'wb') as f:
    pickle.dump({'model': model}, f)