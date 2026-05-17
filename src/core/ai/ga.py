import random
import numpy as np

from . import config


def roulette_selection(pop_scored):
    total = sum(fit for _, fit in pop_scored)
    if total <= 0:
        return random.choice(pop_scored)[0]
    r = random.uniform(0.0, total)
    acc = 0.0
    for genome, fit in pop_scored:
        acc += fit
        if acc >= r:
            return genome
    return pop_scored[-1][0]


def tournament_selection(pop_scored, k=config.TOURNAMENT_K):
    contenders = random.sample(pop_scored, k)
    return max(contenders, key=lambda t: t[1])[0]


def select_parent(pop_scored):
    if config.SELECTION == "tournament":
        return tournament_selection(pop_scored)
    return roulette_selection(pop_scored)


def one_point_crossover(g1, g2):
    if random.random() > config.CROSSOVER_RATE:
        return g1.copy()
    point = random.randint(1, config.GENOME_SIZE - 1)
    child = np.empty_like(g1)
    child[:point] = g1[:point]
    child[point:] = g2[point:]
    return child


def uniform_crossover(g1, g2):
    if random.random() > config.CROSSOVER_RATE:
        return g1.copy()
    mask = np.random.rand(config.GENOME_SIZE) < 0.5
    return np.where(mask, g1, g2).astype(np.float32)


def crossover(g1, g2):
    if config.CROSSOVER == "uniform":
        return uniform_crossover(g1, g2)
    return one_point_crossover(g1, g2)


def mutate(g):
    mask = np.random.rand(config.GENOME_SIZE) < config.MUTATION_RATE
    noise = np.random.randn(config.GENOME_SIZE).astype(np.float32) * config.MUTATION_STRENGTH
    return g + mask * noise


def evolve(population, fitnesses):
    pop_scored = list(zip(population, fitnesses))
    pop_scored.sort(key=lambda t: t[1], reverse=True)
    new_pop = [g.copy() for g, _ in pop_scored[:config.ELITE_COUNT]]
    while len(new_pop) < config.POP_SIZE:
        p1 = select_parent(pop_scored)
        p2 = select_parent(pop_scored)
        new_pop.append(mutate(crossover(p1, p2)))
    return new_pop
