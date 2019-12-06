import logging

import keras as ks
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple
from pathlib import Path

from sklearn.model_selection import train_test_split

from utils import timer, configure_logger

DataPair = Tuple[np.ndarray, np.ndarray]


def load_data() -> Tuple[DataPair, DataPair, DataPair]:
    train, test = ks.datasets.mnist.load_data()
    x_train, x_valid, y_train, y_valid = train_test_split(
        *train, test_size=0.2, random_state=42)
    return (x_train, y_train), (x_valid, y_valid), test


def get_model() -> ks.Sequential:
    model = ks.Sequential()
    model.add(
        ks.layers.Conv2D(
            16, kernel_size=(3, 3), activation="relu", input_shape=(28, 28,
                                                                    1)))
    model.add(ks.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"))
    model.add(ks.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(ks.layers.Dropout(0.25))
    model.add(ks.layers.Flatten())
    model.add(ks.layers.Dense(64, activation="relu"))
    model.add(ks.layers.Dropout(0.3))
    model.add(ks.layers.Dense(10, activation="softmax"))
    model.compile(
        loss="categorical_crossentropy",
        optimizer=ks.optimizers.Adam(),
        metrics=["accuracy"])
    return model


def preprocess(train: DataPair, valid: DataPair,
               test: DataPair) -> Tuple[DataPair, DataPair, DataPair]:
    x_train = train[0].reshape(len(train[0]), 28, 28, 1).astype(np.float32)
    x_valid = valid[0].reshape(len(valid[0]), 28, 28, 1).astype(np.float32)
    x_test = test[0].reshape(len(test[0]), 28, 28, 1).astype(np.float32)

    y_train = ks.utils.to_categorical(train[1], num_classes=10)
    y_valid = ks.utils.to_categorical(valid[1], num_classes=10)
    y_test = ks.utils.to_categorical(test[1], num_classes=10)

    x_train /= 255
    x_valid /= 255
    x_test /= 255

    return (x_train, y_train), (x_valid, y_valid), (x_test, y_test)


if __name__ == "__main__":
    configure_logger(config_name="mnist.log", log_dir="log", debug=True)

    output_dir = Path("artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    log_dir = Path("log")
    log_dir.mkdir(parents=True, exist_ok=True)

    with timer(name="load data", log=True):
        train, valid, test = preprocess(*load_data())

    with timer(name="load model", log=True):
        model = get_model()

    with timer(name="training", log=True):
        history = model.fit(
            train[0],
            train[1],
            batch_size=128,
            epochs=10,
            verbose=1,
            validation_data=valid)

    model.save(str(output_dir / "mnist.h5"))

    score = model.evaluate(test[0], test[1], verbose=0)
    logging.info(f"Test score: {score[1]:.4f}")

    plt.figure(figsize=(10, 10))
    plt.plot(history.history["acc"], marker=".", label="acc")
    plt.plot(history.history['val_acc'], marker='.', label='val_acc')
    plt.title('model accuracy')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(loc='best')
    plt.savefig(log_dir / "mnist_acc.png")

    plt.figure(figsize=(10, 10))
    plt.plot(history.history['loss'], marker='.', label='loss')
    plt.plot(history.history['val_loss'], marker='.', label='val_loss')
    plt.title('model loss')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(loc='best')
    plt.savefig(log_dir / "mnist_loss.png")
