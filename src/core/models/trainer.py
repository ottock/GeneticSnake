import os
import random
import numpy as np

from ..ai import config
from ..ai.pontuacao import pontuacao
from ..ai.ga import evolve
from ..ai.policy import random_chromosome
from .snake import Snake


class Trainer:
    def __init__(self, pop_size=None):
        if pop_size is None:
            pop_size = config.POP_SIZE
        self.population = [random_chromosome() for _ in range(pop_size)]
        self.generation = 1
        self.best_ever_score = 0
        self.best_ever_generation = 0
        self.avg_pontuacao = 0.0
        self._begin_generation()


    def _begin_generation(self):
        self.idx = 0
        self.pontuacoes = [0.0] * len(self.population)
        self.gen_best_score = 0
        self.gen_best_pontuacao = float("-inf")
        self.gen_best_chromosome = None
        self.gen_food_seed = random.randrange(10 ** 9)
        self.snake = Snake(self.population[0], food_seed=self.gen_food_seed)


    def _finalize_current(self):
        p = pontuacao(self.snake.steps, self.snake.score)
        self.pontuacoes[self.idx] = p
        if self.snake.score > self.gen_best_score:
            self.gen_best_score = self.snake.score
        if p > self.gen_best_pontuacao:
            self.gen_best_pontuacao = p
            self.gen_best_chromosome = self.population[self.idx]
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
        self.avg_pontuacao = (sum(self.pontuacoes)
                              / max(1, len(self.pontuacoes)))
        summary = {
            "generation":      self.generation,
            "best_score":      self.gen_best_score,
            "best_pontuacao":  self.gen_best_pontuacao,
            "best_chromosome": self.gen_best_chromosome,
            "avg_pontuacao":   self.avg_pontuacao,
        }
        self.population = evolve(self.population, self.pontuacoes)
        self.generation += 1
        self._begin_generation()
        return summary


    def current_pontuacao(self):
        return pontuacao(self.snake.steps, self.snake.score)


def save_best(chromosome, generation, score, pontuacao_val):
    os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)
    np.save(os.path.join(config.CHECKPOINT_DIR, "snake_best.npy"), chromosome)
    log = os.path.join(config.CHECKPOINT_DIR, "snake_log.csv")
    write_header = not os.path.exists(log)
    with open(log, "a", encoding="utf-8") as f:
        if write_header:
            f.write("geracao,melhor_comidas,melhor_pontuacao\n")
        f.write(f"{generation},{score},{pontuacao_val:.2f}\n")
