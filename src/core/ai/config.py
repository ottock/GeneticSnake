import os

# --- Tabuleiro / regras do jogo ---
GRID_W, GRID_H = 20, 20
MAX_STEPS_PER_FOOD = 150
VISION_RANGE = 8

# Direcoes: 0=cima 1=baixo 2=esquerda 3=direita
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
LEFT_TURN  = {0: 2, 2: 1, 1: 3, 3: 0}
RIGHT_TURN = {0: 3, 3: 1, 1: 2, 2: 0}

# --- Cromossomo da cobra ---
# Cada cobra (individuo) tem um cromossomo = vetor de 8 pesos. Cada peso
# pondera uma feature do estado resultante de cada acao possivel (esquerda,
# reto, direita). A acao de maior pontuacao (cromossomo . features) e'
# escolhida.
ACTION_COUNT = 3
FEATURE_COUNT = 8
CHROMOSOME_SIZE = FEATURE_COUNT

# Nome curto de cada bit do cromossomo (mesma ordem das features)
FEATURE_LABELS = (
    "morre",
    "1/dist_parede",
    "1/dist_corpo",
    "comida_visao",
    "alinha_comida",
    "aproxima",
    "densidade",
    "bias",
)

# Descricao longa de cada bit do cromossomo, exibida no painel
FEATURE_DESCRIPTIONS = (
    "1 se a acao mata a cobra",
    "inverso da dist. ate a parede",
    "inverso da dist. ate o corpo",
    "1 se comida esta na linha de visao",
    "cosseno do angulo com a comida",
    "1 se acao aproxima da comida",
    "fracao de celulas vizinhas com corpo",
    "termo constante (offset)",
)

# --- Parametros do Algoritmo Genetico ---
POP_SIZE = 10           # tamanho da populacao por geracao
MUTATION_RATE = 0.15    # probabilidade de cada bit do cromossomo sofrer mutacao
MUTATION_STRENGTH = 0.25  # intensidade da mutacao
CROSSOVER_RATE = 0.85   # probabilidade de cruzamento (senao copia o pai 1)
CROSSOVER = "um_ponto"  # "um_ponto" ou "uniforme"

# Selecao por roleta (Monte Carlo): unica estrategia.
SELECTION = "roleta"

CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints")
