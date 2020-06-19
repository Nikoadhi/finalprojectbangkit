# -*- coding: utf-8 -*-
"""finalproject

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Nikoadhi/finalprojectbangkit/blob/master/finalproject.ipynb
"""

import os
import zipfile
import random
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile

from google.colab import files
uploaded = files.upload()

import zipfile
import io
zf = zipfile.ZipFile(io.BytesIO(uploaded['Kaggle_Car_Bus.zip']), "r")
zf.extractall()

print(len(os.listdir('/content/Training_set/Training_set/electric bus')))
print(len(os.listdir('/content/Training_set/Training_set/electric car')))
print(len(os.listdir('/content/test/test/electric bus')))
print(len(os.listdir('/content/test/test/electric car')))

model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
model.summary()

TRAINING_DIR = "/content/Training_set/Training_set"
train_datagen = ImageDataGenerator(rescale=1.0/255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')
train_generator = train_datagen.flow_from_directory(TRAINING_DIR,
                                                    batch_size=32,
                                                    class_mode='binary',
                                                    target_size=(150, 150))


VALIDATION_DIR = "/content/test/test"
validation_datagen = ImageDataGenerator(rescale = 1.0/255. )
validation_generator = validation_datagen.flow_from_directory(VALIDATION_DIR,
                                                         batch_size=32,
                                                         class_mode  = 'binary',
                                                         target_size = (150, 150))

class callbacks(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('acc')>0.90):
          print("\nReached 90.0% accuracy so cancelling training!")
          self.model.stop_training = True

callbacks = callbacks()
history = model.fit_generator(train_generator,                      
                              epochs=50,
                              verbose=1,
                              steps_per_epoch = 40,
                              validation_data=validation_generator,
                              callbacks=[callbacks])

test_image = image.load_img('/content/test/test/electric bus/images-306.jpeg', target_size = (150, 150))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = np.array(model.predict(test_image))
train_generator.class_indices
label = (result>0.5).astype(np.int)
CLASSES = ['Car', 'Bus']
print(CLASSES[label[0][0]])

# Commented out IPython magic to ensure Python compatibility.
# PLOT LOSS AND ACCURACY
# %matplotlib inline

import matplotlib.image  as mpimg
import matplotlib.pyplot as plt

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc=history.history['acc']
val_acc=history.history['val_acc']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot(epochs, acc, 'r', "Training Accuracy")
plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training and validation accuracy')
plt.figure()

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.plot(epochs, loss, 'r', "Training Loss")
plt.plot(epochs, val_loss, 'b', "Validation Loss")


plt.title('Training and validation loss')

# Desired output. Charts with training and validation metrics. No crash :)

model.save('finalprojectbangkit.h5')

from google.colab import files
files.download("finalprojectbangkit.h5")