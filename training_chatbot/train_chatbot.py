import random
import json
import pickle
import numpy as np
import pandas as pd

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

# Load intents JSON
with open('intents.json', encoding="utf-8") as json_file:
    intents = json.load(json_file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Tokenization & Lemmatization
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatization & Sorting
words = sorted(set([lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]))
classes = sorted(set(classes))

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffle and convert to NumPy array
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# Model Creation
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Fix Optimizer Parameters
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)  # Removed `decay`
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train Model
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save Model
model.save('chatbotmodel.h5')
print('Training Done')
