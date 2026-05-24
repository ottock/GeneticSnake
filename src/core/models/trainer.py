import os
import random
import numpy as np

from ..ai import config
from ..ai.aptidao import aptidao
from ..ai.ga import evoluir
from ..ai.policy import random_chromosome
from .snake import Snake


class Trainer:
    def __init__(self, sol_por_pop=None):
        if sol_por_pop is None:
            sol_por_pop = config.SOL_POR_POP
        # Criando a populacao inicial (uma lista de cromossomos 1D).
        self.population = [random_chromosome() for _ in range(sol_por_pop)]
        self.generation = 1
        self.best_ever_score = 0
        self.best_ever_generation = 0
        self.media_aptidao = 0.0
        self._begin_generation()


    def _begin_generation(self):
        self.idx = 0
        # Aptidao de cada cromossomo na populacao (preenchida ao longo da
        # geracao, conforme cada cobra termina sua simulacao).
        self.aptidoes = [0.0] * len(self.population)
        self.gen_best_score = 0
        self.gen_best_aptidao = float("-inf")
        self.gen_best_chromosome = None
        self.gen_food_seed = random.randrange(10 ** 9)
        self.snake = Snake(self.population[0], food_seed=self.gen_food_seed)


    def _finalize_current(self):
        a = aptidao(self.snake.steps, self.snake.score)
        self.aptidoes[self.idx] = a
        if self.snake.score > self.gen_best_score:
            self.gen_best_score = self.snake.score
        if a > self.gen_best_aptidao:
            self.gen_best_aptidao = a
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
        # Melhor resultado na iteracao atual.
        self.media_aptidao = (sum(self.aptidoes)
                              / max(1, len(self.aptidoes)))
        summary = {
            "generation":      self.generation,
            "best_score":      self.gen_best_score,
            "best_aptidao":    self.gen_best_aptidao,
            "best_chromosome": self.gen_best_chromosome,
            "media_aptidao":   self.media_aptidao,
        }
        # Criar a nova populacao com base nos pais e filhos.
        self.population = evoluir(self.population, self.aptidoes)
        self.generation += 1
        self._begin_generation()
        return summary


    def current_aptidao(self):
        return aptidao(self.snake.steps, self.snake.score)


def save_best(chromosome, generation, score, aptidao_val):
    os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)
    np.save(os.path.join(config.CHECKPOINT_DIR, "snake_best.npy"), chromosome)
    log = os.path.join(config.CHECKPOINT_DIR, "snake_log.csv")
    write_header = not os.path.exists(log)
    with open(log, "a", encoding="utf-8") as f:
        if write_header:
            f.write("geracao,melhor_comidas,melhor_aptidao\n")
        f.write(f"{generation},{score},{aptidao_val:.2f}\n")
