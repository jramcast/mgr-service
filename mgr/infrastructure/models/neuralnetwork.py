from typing import List

import numpy as np
import keras
from keras.models import Model as KerasModel
from keras.layers import (Activation, BatchNormalization, Dense, Dropout,
                          Flatten, Input)

from ...usecases.interfaces import Model
from ...domain.entities import Prediction, AudioSegment
from .. import embeddings
from ..ontology import MUSIC_GENRE_CLASSES


class NeuralNetworkModel(Model):

    def __init__(self, num_units=768, drop_rate=0.5):
        model_file = "./mgr/infrastructure/models/bal_deep_wt.h5"
        self.num_units = num_units
        self.drop_rate = drop_rate

        inputs = Input(shape=(10, 128))
        outputs = self._define_layers(inputs)
        self.model = KerasModel(inputs=inputs, outputs=outputs)
        self.model.load_weights(model_file)

    def preprocess(self, segments: List[AudioSegment]):
        # At this point, both the full clip and its segments
        # are supossed to be downloaded
        x = np.array(
            [embeddings.extract(segment.filename) for segment in segments]
        )
        return x

    def classify(
        self, features: np.ndarray
    ) -> List[List[Prediction]]:
        """
        Returns a list of list of predictions
        The first list is the list of samples(segments)
        The second list is the list of labels for each segment
        """
        result = self.model.predict(features)

        predictions = []
        for i, record in enumerate(result):
            segment_predictions = []
            predictions.append(segment_predictions)
            for j, prediction in enumerate(record):
                segment_predictions.append(Prediction(
                    MUSIC_GENRE_CLASSES[j]["name"],
                    result[i][j]
                ))

        return predictions

    def _define_layers(self, input):
        # The input layer flattens the 10 seconds as a single dimension of 1280
        reshape = Flatten(input_shape=(-1, 10, 128))(input)

        l1 = Dense((self.num_units))(reshape)
        l1 = BatchNormalization()(l1)
        l1 = Activation('relu')(l1)
        l1 = Dropout(self.drop_rate)(l1)

        l2 = Dense(self.num_units)(l1)
        l2 = BatchNormalization()(l2)
        l2 = Activation('relu')(l2)
        l2 = Dropout(self.drop_rate)(l2)

        classes_num = len(MUSIC_GENRE_CLASSES)
        output_layer = Dense(classes_num, activation='sigmoid')(l2)
        return output_layer
