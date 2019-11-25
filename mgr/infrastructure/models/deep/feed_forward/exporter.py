import os

import tensorflow as tf
from keras.models import Model as KerasModel
from keras import backend as K
from keras.layers import Input

from .layers import define_layers


def export():
    inputs = Input(shape=(10, 128), name="embeddings")
    outputs = define_layers(inputs)

    model = KerasModel(inputs=inputs, outputs=outputs)
    model.load_weights(get_model_file())

    tf.saved_model.simple_save(
        K.get_session(),
        get_exported_path(),
        inputs={'embeddings': model.input},
        outputs={"genres": model.outputs[0]})


def get_model_file():
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, "weights", "unbal_deep_wt.h5")


def get_exported_path():
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, ".tfmodel", "1")


if __name__ == "__main__":
    export()
