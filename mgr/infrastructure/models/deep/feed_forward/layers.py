from keras.layers import (Activation, BatchNormalization, Dense, Dropout,
                          Flatten)

from mgr.infrastructure.audioset.ontology import MUSIC_GENRE_CLASSES


num_units = 768
drop_rate = 0.5


def define_layers(input):
    # The input layer flattens the 10 seconds as a single dimension of 1280
    reshape = Flatten(input_shape=(-1, 10, 128))(input)

    l1 = Dense((num_units))(reshape)
    l1 = BatchNormalization()(l1)
    l1 = Activation('relu')(l1)
    l1 = Dropout(drop_rate)(l1)

    l2 = Dense(num_units)(l1)
    l2 = BatchNormalization()(l2)
    l2 = Activation('relu')(l2)
    l2 = Dropout(drop_rate)(l2)

    classes_num = len(MUSIC_GENRE_CLASSES)
    output_layer = Dense(classes_num, activation='sigmoid')(l2)
    return output_layer
