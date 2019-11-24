import tensorflow as tf

from keras.models import Model as KerasModel
from keras import backend as K
from keras.layers import Input
from .layers import define_layers


def export():
    inputs = Input(shape=(10, 128), name="embeddings")
    outputs = define_layers(inputs)

    model_file = "./mgr/infrastructure/models/unbal_deep_wt.h5"
    model = KerasModel(inputs=inputs, outputs=outputs)
    model.load_weights(model_file)

    tf.saved_model.simple_save(
        K.get_session(),
        "./exported_tfserving_model/1",
        inputs={'embeddings': model.input},
        outputs={"genres": model.outputs[0]})


if __name__ == "__main__":
    export()
