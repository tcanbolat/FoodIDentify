from common.common import food_list, time_stamp

from keras.applications import mobilenet_v2
from keras.backend import clear_session
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

import pandas as pd
import numpy as np

clear_session()

image_size = (244, 244)

data_gen = ImageDataGenerator(rotation_range=30, rescale=1./255, validation_split=0.2)
train_gen = data_gen.flow_from_directory('meta/training-data/train', target_size=image_size, shuffle=True, seed=42)
test_gen = data_gen.flow_from_directory('meta/training-data/test', target_size=image_size, shuffle=True, seed=42)


try:
  model = load_model("model/model/food_model.h5")
except:
  input_shape = [224,224,3]

  transfer_learning_model = mobilenet_v2.MobileNetV2(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
  )

  transfer_learning_model.trainable = False

  model = Sequential([
    transfer_learning_model,
    GlobalAveragePooling2D(),
    Dropout(0.25),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.1),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.1),
    Dense(len(food_list), activation='softmax')
  ])

  model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['AUC'])


model.summary()

earlystopping = EarlyStopping(monitor='val_loss', min_delta=0.001, patience=5, restore_best_weights=True)

checkpoint = ModelCheckpoint(
  filepath='model/food_model_weight_' + time_stamp() + '.hdf5',
  verbose=1,
  save_best_only=True,
  save_weights_only=True
)

BATCH_SIZE = 128
EPOCHS = 15

history = model.fit(
  train_gen,
  steps_per_epoch=train_gen.samples // BATCH_SIZE // 2,
  validation_data=test_gen,
  validation_steps= test_gen.samples // BATCH_SIZE // 2,
  epochs=EPOCHS,
  verbose=1,
  shuffle=True,
  callbacks=[checkpoint, earlystopping]
)

history_df = pd.DataFrame(history.history)
history_df.loc[:,['auc', 'val_auc']].plot()

max_val_auc = max(history_df['val_auc'])
file_name = 'food_model_{:.2f}_{}.h5'.format(max_val_auc, time_stamp())
history_file_name = 'food_model_history_{:.2f}_{}.npy'.format(max_val_auc, time_stamp())

np.save('model/' + history_file_name, history.history) # Saving history object of models testing and validation
model.save('model/' + file_name) # Saving model / used in predict.py
model.save('model/' + 'food_model_{:.2f}_{}'.format(max_val_auc, time_stamp())) # Complete Tensorflow object to deploy with TFLite, TensorFlow.js, TensorFlow Serving, or TFHub

print("Training Complete : Model Saved")
print("Model Accuracy: " + str(max(history_df['val_auc'])))
