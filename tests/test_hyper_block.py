from unittest import mock

import autokeras as ak
import pytest

import numpy as np
import tensorflow as tf


@pytest.fixture(scope='module')
def tmp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('test_hyper_block')


@mock.patch('kerastuner.engine.tuner.Tuner.search',
            side_effect=lambda *args, **kwargs: None)
def test_resnet_block(_, tmp_dir):
    x_train = np.random.rand(100, 32, 32, 3)
    y_train = np.random.randint(10, size=100)
    y_train = tf.keras.utils.to_categorical(y_train)

    input_node = ak.Input()
    output_node = input_node
    output_node = ak.ResNetBlock()(output_node)
    output_node = ak.ClassificationHead()(output_node)

    graph = ak.GraphAutoModel(input_node, output_node,
                              directory=tmp_dir,
                              max_trials=1)
    graph.fit(x_train, y_train,
              epochs=1,
              batch_size=100,
              verbose=False,
              validation_split=0.2)


@mock.patch('kerastuner.engine.tuner.Tuner.search',
            side_effect=lambda *args, **kwargs: None)
def test_xception_block(_, tmp_dir):
    x_train = np.random.rand(100, 32, 32, 3)
    y_train = np.random.randint(10, size=100)
    y_train = tf.keras.utils.to_categorical(y_train)

    input_node = ak.Input()
    output_node = input_node
    output_node = ak.XceptionBlock()(output_node)
    output_node = ak.ClassificationHead()(output_node)

    input_node.shape = (32, 32, 3)
    output_node[0].shape = (10,)

    graph = ak.GraphAutoModel(input_node, output_node,
                              directory=tmp_dir,
                              max_trials=1)
    graph.fit(x_train, y_train,
              epochs=1,
              batch_size=100,
              verbose=False,
              validation_split=0.2)


def test_conv_block(tmp_dir):
    x_train = np.random.rand(100, 3, 3, 3)
    y_train = np.random.randint(10, size=100)
    y_train = tf.keras.utils.to_categorical(y_train)

    input_node = ak.Input()
    output_node = input_node
    output_node = ak.ConvBlock()(output_node)
    output_node = ak.ClassificationHead()(output_node)

    input_node.shape = (3, 3, 3)
    output_node[0].shape = (10,)

    graph = ak.GraphAutoModel(input_node, output_node,
                              directory=tmp_dir,
                              max_trials=1)
    graph.fit(x_train, y_train,
              epochs=1,
              batch_size=100,
              verbose=False,
              validation_split=0.2)
    result = graph.predict(x_train)

    assert result.shape == (100, 10)

# def test_rnn_block(tmp_dir):
#     x_train = np.random.rand(100, 32, 10, 10)
#     y_train = np.random.randint(5, size=100)
#     y_train = tf.keras.utils.to_categorical(y_train)
#
#     input_node = ak.Input()
#     output_node = input_node
#     output_node = ak.RNNBlock()(output_node)
#     output_node = ak.ClassificationHead()(output_node)
#
#     input_node.shape = (32, 10, 10)
#     output_node[0].shape = (5,)
#
#     graph = ak.GraphAutoModel(input_node, output_node,
#                               directory=tmp_dir,
#                               max_trials=1)
#     graph.fit(x_train, y_train,
#               epochs=1,
#               batch_size=100,
#               verbose=False,
#               validation_split=0.2)
#     result = graph.predict(x_train)
#
#     assert result.shape == (100, 5)
#
