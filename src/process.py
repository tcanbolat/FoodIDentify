import tensorflow
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras.models import Sequential
from keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
import pandas as pd

tensorflow.keras.backend.clear_session()

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
model.add(Dense(64, activation="selu")) # 64 units
model.add(Dropout(0.3))
model.add(BatchNormalization(synchronized=True))
model.add(Dense(101, activation='softmax'))

model.summary()

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

earlystopping = EarlyStopping(min_delta=0.001, patience=5, restore_best_weights=True)

checkpoint = ModelCheckpoint(filepath='food_model.hdf5', verbose=1, save_best_only=True, save_weights_only=True)

history = model.fit(train_gen, validation_data=test_gen, epochs=10, verbose=1, callbacks=[checkpoint, earlystopping])

model.save('food_model.h5')

history_df = pd.DataFrame(history.history)
history_df.loc[:,['loss', 'val_loss']].plot()
history_df.loc[:,['accuracy', 'val_accuracy']].plot()

print(max(history_df['val_accuracy']))
