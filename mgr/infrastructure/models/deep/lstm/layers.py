
from keras.layers import (Activation, BatchNormalization, Dense, Dropout,
                          Input, LSTM)

from mgr.infrastructure.audioset.ontology import MUSIC_GENRE_CLASSES

num_units = 768
drop_rate = 0.5


def define_layers(inputs):
    l1 = LSTM(1280, return_sequences=False)(inputs)
    l1 = BatchNormalization()(l1)
    l1 = Activation("relu")(l1)
    l1 = Dropout(drop_rate)(l1)

    classes_num = len(MUSIC_GENRE_CLASSES)
    outputs = Dense(classes_num, activation="sigmoid")(l1)
    return outputs
