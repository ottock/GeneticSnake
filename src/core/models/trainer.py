import os
import random
import numpy as np

from ..ai import config
from ..ai.fitness import fitness_value
from ..ai.ga import evolve
from ..ai.network import random_genome
from .snake import Snake


class Trainer:
    def __init__(self, pop_size=None):
        if pop_size is None:
            pop_size = config.POP_SIZE
        self.population = [random_genome() for _ in range(pop_size)]
        self.generation = 1
        self.best_ever_score = 0
        self.best_ever_generation = 0
        self.avg_fitness = 0.0
        self._begin_generation()


    def _begin_generation(self):
        self.idx = 0
        self.fitnesses = [0.0] * len(self.population)
        self.gen_best_score = 0
        self.gen_best_fitness = float("-inf")
        self.gen_best_genome = None
        self.gen_food_seed = random.randrange(10 ** 9)
        self.snake = Snake(self.population[0], food_seed=self.gen_food_seed)


    def _finalize_current(self):
        fit = fitness_value(self.snake.steps, self.snake.score)
        self.fitnesses[self.idx] = fit
        if self.snake.score > self.gen_best_score:
            self.gen_best_score = self.snake.score
        if fit > self.gen_best_fitness:
            self.gen_best_fitness = fit
            self.gen_best_genome = self.population[self.idx]
        if self.snake.score > self.best_ever_score:
            self.best_ever_score = self.snake.score
            self.best_ever_generation = self.generation


    def step(self):
        self.snake.step()
        if not self.snake.alive:
            self._finalize_current()
            return False
        return True


    def next_individual(self):
        self.idx += 1
        if self.idx >= len(self.population):
            return False
        self.snake = Snake(self.population[self.idx],
                           food_seed=self.gen_food_seed)
        return True


    def advance_generation(self):
        self.avg_fitness = sum(self.fitnesses) / max(1, len(self.fitnesses))
        summary = {
            "generation":  self.generation,
            "best_score":  self.gen_best_score,
            "best_fitness": self.gen_best_fitness,
            "best_genome": self.gen_best_genome,
            "avg_fitness": self.avg_fitness,
        }
        self.population = evolve(self.population, self.fitnesses)
        self.generation += 1
        self._begin_generation()
        return summary


    def current_fitness(self):
        return fitness_value(self.snake.steps, self.snake.score)


def save_best(genome, generation, score, fitness):
    os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)
    np.save(os.path.join(config.CHECKPOINT_DIR, "snake_best.npy"), genome)
    log = os.path.join(config.CHECKPOINT_DIR, "snake_log.csv")
    write_header = not os.path.exists(log)
    with open(log, "a", encoding="utf-8") as f:
        if write_header:
            f.write("generation,best_score,best_fitness\n")
        f.write(f"{generation},{score},{fitness:.2f}\n")