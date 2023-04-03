import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Conv2D, MaxPool2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import pandas as pd

image_size = (235, 235)

data_gen = ImageDataGenerator(rotation_range=30, rescale=1./255, validation_split=0.2)
train_gen = data_gen.flow_from_directory('meta/training-data/train', target_size=image_size) # default mode categorical
test_gen = data_gen.flow_from_directory('meta/training-data/test', target_size=image_size) # default batch_size is 32


input_shape = (235, 235, 3) # 235, 235 stands for w and h. The 3 stands for the three channels for RGB
inception_model = InceptionV3(weights="imagenet", input_shape=input_shape, include_top=False)

inception_model.trainable = False # freeze weights



model = Sequential()
model.add(inception_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(64, activation="relu")) # 64 units
model.add(Dropout(0.3))
model.add(Dense(3, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

earlystopping = EarlyStopping(min_delta=0.001, patience=5, restore_best_weights=True)

checkpoint = ModelCheckpoint(filepath='food_model.hdf5', verbose=1, save_best_only=True, save_weights_only=True)

history = model.fit(train_gen, validation_data=test_gen, epochs=30, verbose=1, callbacks=[checkpoint, earlystopping])

history_df = pd.DataFrame(history.history)
history_df.loc[:,['loss', 'val_loss']].plot()
history_df.loc[:,['accuracy', 'val_accuracy']].plot()

print(max(history_df['val_accuracy']))
