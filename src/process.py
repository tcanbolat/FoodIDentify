import tensorflow
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization, Conv2D, MaxPool2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
import pandas as pd

tensorflow.keras.backend.clear_session()

image_size = (235, 235)

data_gen = ImageDataGenerator(rotation_range=30, rescale=1./235, validation_split=0.2)
train_gen = data_gen.flow_from_directory('meta/training-data/train', target_size=image_size) # default mode categorical
test_gen = data_gen.flow_from_directory('meta/training-data/test', target_size=image_size) # default batch_size is 32


try:
  model = load_model("food_model.h5")
except:
  input_shape = (235, 235, 3) # 235, 235 stands for w and h. The 3 stands for the three channels for RGB
  inception_model = InceptionV3(weights="imagenet", input_shape=input_shape, include_top=False)

  inception_model.trainable = False # freeze weights

  # model = Sequential()
  # model.add(inception_model)
  # model.add(GlobalAveragePooling2D())
  # model.add(Dense(64, activation="relu")) # 64 units
  # model.add(Dropout(0.3))
  # model.add(BatchNormalization())
  # model.add(Dense(42, activation='softmax'))

  model = Sequential()
  model.add(inception_model)
  model.add(Dropout(0.2))

  model.add(Conv2D(512, 2, activation='relu'))  #filters=32, strides=2, kernel_size=(5,5),
  model.add(MaxPool2D(pool_size=(2,2)))
  model.add(Dropout(0.2))

  model.add(Conv2D(512, 2, activation='relu'))
  model.add(GlobalAveragePooling2D()) # avg output of feature map

  model.add(Dense(42, activation='softmax'))



  model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])


model.summary()

earlystopping = EarlyStopping(min_delta=0.001, patience=5, restore_best_weights=True)

checkpoint = ModelCheckpoint(filepath='food_model.hdf5', verbose=1, save_best_only=True, save_weights_only=True)

history = model.fit(train_gen, validation_data=test_gen, epochs=15, verbose=1, callbacks=[checkpoint, earlystopping])

model.save('food_model.h5')

history_df = pd.DataFrame(history.history)
history_df.loc[:,['loss', 'val_loss']].plot()
history_df.loc[:,['accuracy', 'val_accuracy']].plot()

print(max(history_df['val_accuracy']))
