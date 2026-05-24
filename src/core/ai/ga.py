"""Algoritmo Genetico: selecao por roleta + cruzamento + mutacao."""

import random
import numpy as np

from . import config


def roulette_selection(pop_scored):
    """Selecao por roleta (Monte Carlo).

    Cada individuo ocupa uma porcao da roleta proporcional a sua pontuacao.
    Maior pontuacao => maior chance de ser escolhido como pai.

    Pontuacoes podem ser negativas (penalidade por passos sem comer); por
    isso deslocamos todos os valores para serem nao-negativos antes da
    roleta, preservando as diferencas proporcionais.
    """
    min_p = min(p for _, p in pop_scored)
    shift = -min_p + 1e-6 if min_p < 0 else 0.0
    total = sum(p + shift for _, p in pop_scored)
    if total <= 0:
        return random.choice(pop_scored)[0]
    r = random.uniform(0.0, total)
    acc = 0.0
    for chromosome, p in pop_scored:
        acc += p + shift
        if acc >= r:
            return chromosome
    return pop_scored[-1][0]


def crossover_um_ponto(c1, c2):
    """Cruzamento em um ponto: divide os pais num ponto aleatorio e combina."""
    if random.random() > config.CROSSOVER_RATE:
        return c1.copy()
    point = random.randint(1, config.CHROMOSOME_SIZE - 1)
    child = np.empty_like(c1)
    child[:point] = c1[:point]
    child[point:] = c2[point:]
    return child


def crossover_uniforme(c1, c2):
    """Cruzamento uniforme: cada bit do filho vem de um dos pais ao acaso."""
    if random.random() > config.CROSSOVER_RATE:
        return c1.copy()
    mask = np.random.rand(config.CHROMOSOME_SIZE) < 0.5
    return np.where(mask, c1, c2).astype(np.float32)


def crossover(c1, c2):
    if config.CROSSOVER == "uniforme":
        return crossover_uniforme(c1, c2)
    return crossover_um_ponto(c1, c2)


def mutate(c):
    """Mutacao: cada bit do cromossomo pode ser alterado por um valor aleatorio."""
    mask = np.random.rand(config.CHROMOSOME_SIZE) < config.MUTATION_RATE
    noise = (np.random.randn(config.CHROMOSOME_SIZE).astype(np.float32)
             * config.MUTATION_STRENGTH)
    return c + mask * noise


def evolve(population, scores):
    """Produz a proxima geracao: roleta + cruzamento + mutacao."""
    pop_scored = list(zip(population, scores))
    new_pop = []
    target_size = len(population)
    while len(new_pop) < target_size:
        p1 = roulette_selection(pop_scored)
        p2 = roulette_selection(pop_scored)
        new_pop.append(mutate(crossover(p1, p2)))
    return new_pop
