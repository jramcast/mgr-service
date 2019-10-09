
import os
import sys
import time
import numpy as np
import tensorflow as tf

from .models.audioset import vggish_input
from .models.audioset import vggish_postprocess
from .models.audioset import vggish_slim
from .models.audioset import vggish_params


flags = tf.app.flags

flags.DEFINE_string(
    'wav_file', None,
    'Path to a wav file. Should contain signed 16-bit PCM samples. '
    'If none is provided, a synthetic sound is used.')

flags.DEFINE_string(
    'checkpoint', 'data/vggish/vggish_model.ckpt',
    'Path to the VGGish checkpoint file.')

FLAGS = flags.FLAGS


NUMBER_OF_SECONDS = 10

def resize_axis(tensor, axis, new_size, fill_value=0):
    """
    Function from YouTube-8m supporting code:
    https://github.com/google/youtube-8m/blob/2c94ed449737c886175a5fff1bfba7eadc4de5ac/readers.py

    Truncates or pads a tensor to new_size on on a given axis.
    Truncate or extend tensor such that tensor.shape[axis] == new_size. If the
    size increases, the padding will be performed at the end, using fill_value.
    Args:
    tensor: The tensor to be resized.
    axis: An integer representing the dimension to be sliced.
    new_size: An integer or 0d tensor representing the new value for
        tensor.shape[axis].
    fill_value: Value to use to fill any new entries in the tensor. Will be
        cast to the type of tensor.
    Returns:
    The resized tensor.
    """
    tensor = tf.convert_to_tensor(tensor)
    shape = tf.unstack(tf.shape(tensor))

    pad_shape = shape[:]
    pad_shape[axis] = tf.maximum(0, new_size - shape[axis])

    shape[axis] = tf.minimum(shape[axis], new_size)
    shape = tf.stack(shape)

    resized = tf.concat([
        tf.slice(tensor, tf.zeros_like(shape), shape),
        tf.fill(tf.stack(pad_shape), tf.cast(fill_value, tensor.dtype))
    ], axis)

    # Update shape.
    new_shape = tensor.get_shape().as_list()  # A copy is being made.
    new_shape[axis] = new_size
    resized.set_shape(new_shape)
    return resized


def extract(wav_file_path):
    # Prepare a postprocessor to munge the model embeddings.
    pproc = vggish_postprocess.Postprocessor(
        "data/vggish/vggish_pca_params.npz"
    )

    with tf.Graph().as_default(), tf.Session() as sess:
        # Define the model in inference mode, load the checkpoint, and
        # locate input and output tensors.
        vggish_slim.define_vggish_slim(training=False)
        vggish_slim.load_vggish_slim_checkpoint(sess, FLAGS.checkpoint)
        features_tensor = sess.graph.get_tensor_by_name(
            vggish_params.INPUT_TENSOR_NAME)
        embedding_tensor = sess.graph.get_tensor_by_name(
            vggish_params.OUTPUT_TENSOR_NAME)

        embedding_tensor = resize_axis(
            embedding_tensor,
            axis=0,
            new_size=NUMBER_OF_SECONDS)

        example_batch = vggish_input.wavfile_to_examples(wav_file_path)

        print(example_batch.shape)
        # Run inference and postprocessing.
        [embedding_batch] = sess.run(
            [embedding_tensor],
            feed_dict={features_tensor: example_batch}
        )

        postprocessed_batch = pproc.postprocess(embedding_batch)
        return postprocessed_batch
