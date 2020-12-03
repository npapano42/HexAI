import os
from sys import stderr

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import callbacks, metrics
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

import gen_test_data
import re


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

# print(model.output_shape) # (None, 1)
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# PLAYERS = {"none": 0, "white": 1, "black": -1}
def load_from_folders():
    """
    Loads games from folders based on winner, named white_wins and black_wins. Both folders MUST be in the root directory of the project
    """
    x = []
    y = []
    loc = "white_wins/"
    for game_file in os.listdir(loc):
        state = gen_test_data.read_from_file(loc + game_file).game
        board = np.expand_dims(state.board, 2)
        x.append(board)
        if re.search("-rollback-", game_file):  # game was rolled back from a win
            moves_rolled_back = int(re.search(r"-(\d+)", game_file).group(0)[1:])
            # the number of moves to the end of the game, closer to actual value as game reaches end
            classification = 0.5 + 0.5 * (len(state.move_list) / (len(state.move_list) + moves_rolled_back))
            y.append(np.asarray([classification]))
        else:
            y.append(np.asarray([1]))

    stderr.write("loaded from white wins\n")
    loc = "black_wins/"
    for game_file in os.listdir(loc):
        state = gen_test_data.read_from_file(loc + game_file).game
        board = np.expand_dims(state.board, 2)
        x.append(board)
        if re.search("-rollback-", game_file):  # game was rolled back from a win
            moves_rolled_back = int(re.search(r"-(\d+)", game_file).group(0)[1:])
            # the number of moves to the end of the game, closer to actual value as game reaches end
            classification = 0.5 - 0.5 * (len(state.move_list) / (len(state.move_list) + moves_rolled_back))
            y.append(np.asarray([classification]))
        else:
            y.append(np.asarray([0]))
    stderr.write("loaded from black wins\n")

    # reshape for input into CNN and return
    return np.array([game for game in x]), np.array([game for game in y])


def train():
    """
    Trains the model. Model architecture is as follows below.

    Uncomment the model.save() line to save the model after training. The model name should not be changed as it is the hard coded in the agent

    Input shape to model is x = (# training examples, 11, 11, 1), y = (# training examples, 1)

    n predictions can be done with shape predict() called on the model with input shape (n, 11, 11, 1), giving an equally-sized (n, 1) shaped output
    """
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

    model.compile(loss=tf.keras.losses.MeanSquaredLogarithmicError(), optimizer=tf.keras.optimizers.Adam(), metrics=[metrics.mean_squared_error])

    model.summary()
    x, y = load_from_folders()
    # early stop to find epoch before overfitting
    early_stop = callbacks.EarlyStopping(monitor="val_loss",
                                         mode="min", patience=10, verbose=2,
                                         restore_best_weights=True)

    # early_stop = callbacks.EarlyStopping(monitor="val_mean_squared_logarithmic_error",
    #                                      mode="min", patience=10, verbose=2,
    #                                      restore_best_weights=True)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
    model_history = model.fit(x=x_train, y=y_train,
                              validation_data=(x_test, y_test),
                              epochs=100, batch_size=32, verbose=1) # callbacks=[early_stop]
    model.save("CNN_hex_model")

    plt.plot(model_history.history['loss'])
    plt.show()
    plt.plot(model_history.history['val_loss'])
    plt.show()
    plt.plot(model_history.history['mean_squared_error'])
    plt.show()
    plt.plot(model_history.history['val_mean_squared_error'])
    plt.show()


if __name__ == "__main__":
    train()
