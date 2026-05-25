"""Algoritmo Genetico: ELITISMO + ROLETA (Monte Carlo).

Estrutura espelhada do material da aula (notebook 'Algoritmos_geneticos'),
combinada com elitismo:

  - cal_pop_aptidao : aptidao de cada individuo da populacao
  - shippar         : seleciona pais via roleta (Monte Carlo)
  - cruzamento      : cruzamento de um ponto (no centro)
  - mutacao         : ruido uniforme em genes espacados
  - evoluir         : driver de uma geracao
                      (top NUM_ELITES intactos + roleta + cruzamento + mutacao)
"""

import numpy as np

from . import config


# APTIDAO
"""A aptidao de cada cromossomo e' calculada no Trainer (ver aptidao.py)
apos a simulacao do jogo. Aqui apenas empacotamos a lista em numpy."""
def cal_pop_aptidao(aptidoes):
    return np.asarray(aptidoes, dtype=np.float64)


# SELECAO POR ROLETA (SHIPPAR)
"""Seleciona 'num_pais' individuos da populacao para serem pais da proxima
geracao usando ROLETA (Monte Carlo).

Cada individuo ocupa uma fatia da roleta proporcional a sua aptidao: maior
aptidao => maior chance de ser escolhido. Aptidoes negativas (ou todas
iguais) sao deslocadas para nao-negativas, preservando as diferencas
proporcionais. As escolhas sao independentes (com reposicao), entao um
mesmo individuo pode ser escolhido como pai mais de uma vez."""
def shippar(pop, aptidao, num_pais):
    pais = np.empty((num_pais, pop.shape[1]), dtype=pop.dtype)
    min_a = float(np.min(aptidao))
    shift = -min_a + 1e-6 if min_a < 0 else 0.0
    roleta = aptidao + shift
    total = float(np.sum(roleta))
    for pais_num in range(num_pais):
        if total <= 0:
            idx = np.random.randint(0, pop.shape[0])
        else:
            r = np.random.uniform(0.0, total)
            acc = 0.0
            idx = pop.shape[0] - 1
            for i in range(pop.shape[0]):
                acc += roleta[i]
                if acc >= r:
                    idx = i
                    break
        pais[pais_num, :] = pop[idx, :]
    return pais


# CRUZAMENTO (um ponto no centro)
"""O ponto em que ocorre o cruzamento entre dois pais. Normalmente, esta no
centro. Cada filho recebe a primeira metade dos genes do pai 1 e a segunda
metade do pai 2."""
def cruzamento(pais, prole_tamanho):
    prole = np.empty(prole_tamanho, dtype=pais.dtype)
    cruzamento_ponto = np.uint8(prole_tamanho[1] / 2)

    for k in range(prole_tamanho[0]):
        # Indices dos dois pais (ja sorteados pela roleta).
        pais1_idx = (2 * k) % pais.shape[0]
        pais2_idx = (2 * k + 1) % pais.shape[0]
        # Primeira metade dos genes vem do pai 1.
        prole[k, 0:cruzamento_ponto] = pais[pais1_idx, 0:cruzamento_ponto]
        # Segunda metade dos genes vem do pai 2.
        prole[k, cruzamento_ponto:] = pais[pais2_idx, cruzamento_ponto:]
    return prole


# MUTACAO
"""A mutacao altera alguns genes (espacados ao longo do cromossomo) somando
um valor aleatorio uniforme. O numero de genes alterados e' definido por
'num_mutacoes'."""
def mutacao(prole_cruzamento, num_mutacoes=1):
    mutacoes_contador = np.uint8(prole_cruzamento.shape[1] / num_mutacoes)
    for idx in range(prole_cruzamento.shape[0]):
        gene_idx = mutacoes_contador - 1
        for _ in range(num_mutacoes):
            random_valor = np.random.uniform(-1.0, 1.0, 1)[0]
            prole_cruzamento[idx, gene_idx] = (
                prole_cruzamento[idx, gene_idx] + random_valor)
            gene_idx = gene_idx + mutacoes_contador
    return prole_cruzamento


# MOTOR GENETICO
def evoluir(populacao, aptidoes):
    """Produz a proxima geracao: elitismo + roleta + cruzamento + mutacao.

    1. Os top NUM_ELITES individuos (maior aptidao) sao copiados INTACTOS
       para a proxima geracao. Garante que a campea nunca se perde.
    2. Os outros (SOL_POR_POP - NUM_ELITES) slots sao filhos: dois pais por
       filho sorteados via roleta (sobre a populacao inteira), combinados
       por cruzamento e mutados.
    """
    pop_tamanho = (len(populacao), config.CHROMOSOME_SIZE)
    pop_atual = np.stack(populacao).astype(np.float32)
    aptidao = cal_pop_aptidao(aptidoes)

    # 1. Elitismo: top NUM_ELITES individuos passam intactos.
    n_elites = min(config.NUM_ELITES, pop_tamanho[0])
    elites_idx = np.argsort(aptidao)[-n_elites:][::-1]
    elites = pop_atual[elites_idx]

    # 2. Filhos: roleta sobre a populacao inteira para escolher os pais
    #    (2 pais por filho) e gerar (pop - n_elites) filhos.
    num_filhos = pop_tamanho[0] - n_elites
    nova = np.empty(pop_tamanho, dtype=np.float32)
    nova[:n_elites] = elites

    if num_filhos > 0:
        pais = shippar(pop_atual, aptidao, 2 * num_filhos)
        prole = cruzamento(pais, prole_tamanho=(num_filhos, pop_tamanho[1]))
        prole = mutacao(prole, num_mutacoes=config.NUM_MUTACOES)
        nova[n_elites:] = prole

    return [row.astype(np.float32) for row in nova]
