import tensorflow as tf
import matplotlib.pyplot as plt
import zipfile
import cv2
import os 
import numpy as np
import matplotlib.image as mpimg
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image


img=image.load_img("image/train/COVID19/COVID19(0).jpg")
plt.imshow(img)

cv2.imread("image/train/COVID19/COVID19(0).jpg").shape
cv2.imread("image/train/COVID19/COVID19(0).jpg")
train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
        'image/train', 
        target_size=(150, 150),  
        batch_size=240, 
        class_mode='binary')


validation_generator = train_datagen.flow_from_directory(
        'image/validation',
        target_size=(150, 150),  
        batch_size=240,
        class_mode='binary')

train_generator.class_indices
train_generator.classes
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

from tensorflow.keras.optimizers import RMSprop


model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['accuracy'])


history = model.fit(
      train_generator,
      steps_per_epoch=1,  
      epochs=20,
      validation_data = validation_generator)

dir_path = "image/test"
for i in os.listdir(dir_path):
    img = image.load_img(dir_path+ '//' + i , target_size=(150,150))
    plt.imshow(img)
    plt.show()
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes =model.predict(images)
    if classes[0]==0:
        print("Covid detected")
 
    else:
        print("Normal")
        
        
dir_path = "image/test"
c=0
n=0

y_pred = []
for i in os.listdir(dir_path):
    img = image.load_img(dir_path+ '//' + i , target_size=(150,150))
   
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes =model.predict(images)
    if classes[0]==0:
        c=c+1
        y_pred.append("covid-19")
 
    else:
        n=n+1
        y_pred.append("Normal")
        
print("Covid:",c)
print("Normal:",n)


import sklearn.metrics
from sklearn.metrics import accuracy_score


y_true = ["covid-19", "covid-19", "covid-19", "covid-19", "covid-19", "Normal", "Normal","Normal","Normal","Normal"]

r = sklearn.metrics.confusion_matrix(y_true, y_pred)
print("confusion_matrix:",r)

score = accuracy_score(y_true, y_pred) * 100
print("Accuracy using CNN: ", round(score, 1), "%") 
print (classification_report(y_true, y_pred))

