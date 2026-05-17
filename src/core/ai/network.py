import numpy as np

from . import config


def random_genome():
    return np.random.randn(config.GENOME_SIZE).astype(np.float32) * 0.5


def genome_to_layers(genome):
    layers, idx = [], 0
    for shape in config.LAYER_SHAPES:
        size = int(np.prod(shape))
        layers.append(genome[idx:idx + size].reshape(shape))
        idx += size
    return [(layers[i], layers[i + 1]) for i in range(0, len(layers), 2)]


def nn_forward(layers, x):
    a = x
    last = len(layers) - 1
    for i, (W, b) in enumerate(layers):
        z = W @ a + b
        a = np.tanh(z) if i < last else z
    return a