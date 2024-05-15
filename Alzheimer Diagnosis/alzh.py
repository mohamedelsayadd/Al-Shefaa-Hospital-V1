import tensorflow as tf 
from tensorflow import keras  
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.image as img 
import tensorflow.keras.backend as K 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.preprocessing import image 
from pylab import imread,subplot,imshow,show 

train = ImageDataGenerator(rescale=1./255) 
test =  ImageDataGenerator(rescale=1./255) 
val =  ImageDataGenerator(rescale=1./255) 

train=r"C:\Users\moham\Desktop\MY AI\Projects\Deep Learning Projects\Alzheimer Diagnosis\train" 

train_data = tf.keras.preprocessing.image_dataset_from_directory( 
    train, 
    validation_split=0.2, 
    image_size=(224,224), 
    batch_size=32, 
    subset='training', 
    seed=1000 )

val=r"C:\Users\moham\Desktop\MY AI\Projects\Deep Learning Projects\Alzheimer Diagnosis\train" 

val_data = tf.keras.preprocessing.image_dataset_from_directory( 
    val, 
    validation_split=0.2, 
    image_size=(224,224), 
batch_size=32, 
subset='validation', 
seed=1000 
) 
test=r"C:\Users\moham\Desktop\MY AI\Projects\Deep Learning Projects\Alzheimer Diagnosis\test"
test_data=tf.keras.preprocessing.image_dataset_from_directory( 
    test, 
    image_size=(224,224), 
batch_size=32, 
seed=1000 
) 

class_names = ['MildDementia', 'ModerateDementia', 'NonDementia', 
'VeryMildDementia'] 

train_data.class_names = class_names 
val_data.class_names = class_names

# print(val_data) 


from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D,Input 
from tensorflow.keras.layers import Dense 

model=Sequential()
model.add(Conv2D(16,(3,3), activation='relu', input_shape=(224,224,3))) 
model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Conv2D(32,(3,3), activation='relu')) 
model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Conv2D(32,(3,3), activation='relu')) 
model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Flatten()) 
model.add(Dense(10,activation='relu')) 
model.add(Dense(5,activation='relu')) 
model.add(Dense(12,activation='relu')) 
model.add(Dense(30,activation='relu')) 
model.add(Dense(10,activation='relu')) 
model.add(Dense(100,activation='relu')) 
model.add(Dense(133,activation='relu')) 
model.add(Dense(4,activation='softmax')) 
model.summary()

model.compile(optimizer = tf.keras.optimizers.Adam(1e-4), 
loss="sparse_categorical_crossentropy", metrics=["accuracy"]) 
history = model.fit(train_data, validation_data=val_data, epochs=15)

model.save("alzh_model2.h5")


for images, labels in val_data.take(1): 
    for i in range(6): 
        print("True_class:",val_data.class_names[labels[i]]) 
        x = image.img_to_array(images[i]) 
        x = np.expand_dims(x, axis=0) 
        p=np.argmax(model.predict(x)) 
        if p==0: 
            print("MRI diagnosis is: Mild Dementia") 
        elif p==1: 
            print("MRI diagnosis is: Moderate Dementia") 
        elif p==2: 
            print("MRI diagnosis is: Non Dementia") 
        else: 
            print("MRI diagnosis is: Very Mild Dementia") 
            print("Predicted class:",p) 
print("All the MRI diagnosis iss are correct!!!!!")