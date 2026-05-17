import os

GRID_W, GRID_H = 20, 20
MAX_STEPS_PER_FOOD = 150

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
RAYS = [(0, -1), (1, -1), (1, 0), (1, 1),
        (0, 1), (-1, 1), (-1, 0), (-1, -1)]
FRONT_RAY = {0: 0, 3: 2, 1: 4, 2: 6}
LEFT_TURN  = {0: 2, 2: 1, 1: 3, 3: 0}
RIGHT_TURN = {0: 3, 3: 1, 1: 2, 2: 0}

INPUT_SIZE = 24
HIDDEN1 = 20
HIDDEN2 = 12
OUTPUT_SIZE = 3

LAYER_SHAPES = [
    (HIDDEN1, INPUT_SIZE),  (HIDDEN1,),
    (HIDDEN2, HIDDEN1),     (HIDDEN2,),
    (OUTPUT_SIZE, HIDDEN2), (OUTPUT_SIZE,),
]

POP_SIZE = 200
ELITE_COUNT = 8
TOURNAMENT_K = 4
MUTATION_RATE = 0.04
MUTATION_STRENGTH = 0.15
CROSSOVER_RATE = 0.85

SELECTION = "roulette"
CROSSOVER = "one_point"

CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints")


def _genome_size():
    n = 0
    for shape in LAYER_SHAPES:
        prod = 1
        for d in shape:
            prod *= d
        n += prod
    return n


GENOME_SIZE = _genome_size()