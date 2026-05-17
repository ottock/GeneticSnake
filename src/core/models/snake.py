import random
import numpy as np
from collections import deque

from ..ai import config
from ..ai.network import genome_to_layers, nn_forward


class Snake:
    def __init__(self, genome, food_seed=None):
        self.genome = genome
        self.layers = genome_to_layers(genome)
        self.food_rng = random.Random(food_seed)
        self.reset()


    def reset(self):
        cx, cy = config.GRID_W // 2, config.GRID_H // 2
        self.body = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
        self.body_set = set(self.body)
        self.direction = 3
        self.alive = True
        self.score = 0
        self.steps = 0
        self.steps_since_food = 0
        self._spawn_food()


    def _spawn_food(self):
        empty = [(x, y)
                 for x in range(config.GRID_W)
                 for y in range(config.GRID_H)
                 if (x, y) not in self.body_set]
        if not empty:
            self.alive = False
            self.food = None
            return
        self.food = self.food_rng.choice(empty)


    def vision(self):
        head = self.body[0]
        body_no_head = self.body_set - {head}
        offset = config.FRONT_RAY[self.direction]
        out = np.zeros(config.INPUT_SIZE, dtype=np.float32)
        for rel in range(8):
            dx, dy = config.RAYS[(offset + rel) % 8]
            x, y = head
            dist = 0
            seen_food = 0.0
            seen_body = 0.0
            while True:
                x += dx
                y += dy
                dist += 1
                if x < 0 or x >= config.GRID_W or y < 0 or y >= config.GRID_H:
                    break
                if seen_food == 0.0 and (x, y) == self.food:
                    seen_food = 1.0
                if seen_body == 0.0 and (x, y) in body_no_head:
                    seen_body = 1.0
            out[rel * 3 + 0] = 1.0 / dist
            out[rel * 3 + 1] = seen_food
            out[rel * 3 + 2] = seen_body
        return out


    def step(self):
        if not self.alive:
            return
        logits = nn_forward(self.layers, self.vision())
        choice = int(np.argmax(logits))
        if choice == 0:
            self.direction = config.LEFT_TURN[self.direction]
        elif choice == 2:
            self.direction = config.RIGHT_TURN[self.direction]

        hx, hy = self.body[0]
        dx, dy = config.MOVES[self.direction]
        nx, ny = hx + dx, hy + dy

        if nx < 0 or nx >= config.GRID_W or ny < 0 or ny >= config.GRID_H:
            self.alive = False
            return

        tail = self.body[-1]
        will_eat = (nx, ny) == self.food
        if (nx, ny) in self.body_set and not (not will_eat and (nx, ny) == tail):
            self.alive = False
            return

        self.body.appendleft((nx, ny))
        self.body_set.add((nx, ny))
        if will_eat:
            self.score += 1
            self.steps_since_food = 0
            self._spawn_food()
        else:
            self.body.pop()
            self.body_set.discard(tail)
            self.steps_since_food += 1

        self.steps += 1
        if self.steps_since_food > config.MAX_STEPS_PER_FOOD + 20 * self.score:
            self.alive = False