import keras
import numpy as np
import tensorflow as tf
from keras.optimizers import SGD
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# input_board = Input(shape=(11, 11, 1))
# print(input_board)
# x = Conv2D(4, (3, 3), activation='relu', padding='same')(input_board)
# x = MaxPooling2D((2, 2), padding='same')(x)                              # shape(x) is now (6,6,4)
# x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
# x = MaxPooling2D((2, 2), padding='same')(x)                              # shape now (3,3,16)
# x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
# x = MaxPooling2D((2, 2), padding='same')(x)                              # shape now (2,2,32)
# x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
# encoded = MaxPooling2D((2, 2), padding='same')(x)                        # shape now (1,1,64)
# flat = Flatten(encoded)
# print(flat)


# input_board = np.zeros((11, 11), dtype=np.int8)

input_board = np.asarray(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 1, 0, 2, 0, 0],
     [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

input_board = np.expand_dims(input_board, 2)

model = tf.keras.Sequential()
model.add(Conv2D(4, (3, 3), strides=1, activation='relu', padding='same', input_shape=(11, 11, 1)))
model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
model.add(Conv2D(16, (3, 3), strides=1, activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
model.add(Conv2D(32, (3, 3), strides=1, activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
model.add(Conv2D(64, (3, 3), strides=1, activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
model.add(Flatten())
model.add(Dense(121))
# print(model.output_shape)
model.compile(loss="mean_squared_error", optimizer=SGD(lr=0.01, momentum=0.9))

model.summary()

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# model.save("MCNN")
