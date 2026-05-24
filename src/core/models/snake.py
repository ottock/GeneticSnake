import random
from collections import deque

from ..ai import config
from ..ai.policy import choose_action


class Snake:
    def __init__(self, chromosome, food_seed=None):
        self.chromosome = chromosome
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


    def step(self):
        if not self.alive:
            return
        choice = choose_action(self.chromosome, self)
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
