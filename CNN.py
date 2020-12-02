import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sys import stderr
from keras import callbacks
from keras.optimizers import SGD
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split

import gen_test_data


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

# input_board = np.asarray(
#     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 1, 0, 2, 0, 0],
#      [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
#
# input_board = np.expand_dims(input_board, 2)


# print(model.output_shape) # (None, 1)
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# model.save("MCNN")

# PLAYERS = {"none": 0, "white": 1, "black": -1}
def load_from_folders():
    x = []
    y = []
    loc = "white_wins/"
    for game_file in os.listdir(loc):
        board = gen_test_data.read_from_file(loc + game_file).game.board
        board = np.expand_dims(board, 2)
        x.append(board)
        y.append(np.asarray([1]))

    stderr.write("loaded from white wins\n")
    loc = "black_wins/"
    for game_file in os.listdir(loc):
        board = gen_test_data.read_from_file(loc + game_file).game.board
        board = np.expand_dims(board, 2)
        x.append(board)
        y.append(np.asarray([1]))
    stderr.write("loaded from black wins\n")

    # reshape for input into CNN and return
    return np.array([game for game in x]), np.array([game for game in y])


def train():
    model = Sequential()
    model.add(Conv2D(4, (3, 3), strides=1, activation='relu', padding='same', input_shape=(11, 11, 1)))
    model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
    model.add(Conv2D(16, (3, 3), strides=1, activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
    model.add(Conv2D(32, (3, 3), strides=1, activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
    model.add(Conv2D(64, (3, 3), strides=1, activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=2, padding='same'))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss="mean_squared_error", optimizer=SGD(lr=0.01, momentum=0.9))

    model.summary()
    x, y = load_from_folders()
    # early stop to find epoch before overfitting
    early_stop = callbacks.EarlyStopping(monitor="val_loss",
                                         mode="min", patience=10, verbose=2,
                                         restore_best_weights=True)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
    model_history = model.fit(x=x_train, y=y_train,
                              validation_data=(x_test, y_test),
                              epochs=1000, batch_size=32, verbose=1, callbacks=[early_stop])
    # model.save("CNN_hex_model")
    print(model_history.history.keys())
    # summarize history for accuracy
    plt.plot(model_history.history['accuracy'])
    plt.plot(model_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(model_history.history['loss'])
    plt.plot(model_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


if __name__ == "__main__":
    train()
