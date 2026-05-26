import os

# --- Tabuleiro / regras do jogo ---
GRID_W, GRID_H = 20, 20
MAX_STEPS_PER_FOOD = 100
VISION_RANGE = 8

# Direcoes: 0=cima 1=baixo 2=esquerda 3=direita
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
LEFT_TURN  = {0: 2, 2: 1, 1: 3, 3: 0}
RIGHT_TURN = {0: 3, 3: 1, 1: 2, 2: 0}

# --- Cromossomo da cobra ---
# Cada cobra (individuo) tem um cromossomo = vetor de pesos. Cada peso
# pondera uma feature do estado resultante de cada acao possivel (esquerda,
# reto, direita). A acao de maior pontuacao (cromossomo . features) e'
# escolhida.
ACTION_COUNT = 3
FEATURE_COUNT = 9
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
    "explora_centro",
    "1/dist_cauda",
)

# Descricao longa de cada bit do cromossomo, exibida no painel
FEATURE_DESCRIPTIONS = (
    "1 se a acao mata a cobra",
    "inverso da dist. ate a parede (<=8 quadrados)",
    "inverso da dist. ate o corpo (<=8 quadrados)",
    "1 se comida na linha de visao (<=8 quadrados)",
    "cosseno com a comida (so se visivel)",
    "1 se acao aproxima da comida (so se visivel)",
    "fracao de celulas vizinhas com corpo",
    "alinha com o centro quando nao ve comida",
    "inverso da dist. ate a cauda propria",
)

# --- Parametros do Algoritmo Genetico ---

# Numero de pesos a otimizar (cada cromossomo tem 'num_pesos' genes).
NUM_PESOS = CHROMOSOME_SIZE

# Quantidade de individuos (cromossomos) por populacao.
SOL_POR_POP = 100

# Numero de mutacoes aplicadas em cada filho (genes espacados).
NUM_MUTACOES = 2

# Numero de individuos do topo do ranking que sao copiados INTACTOS para a
# proxima geracao (elitismo). Garante que a melhor cobra nunca se perde por
# culpa da roleta ou de uma mutacao ruim.
NUM_ELITES = 10

# Numero de geracoes (informativo; o jogo treina indefinidamente).
NUM_GERACOES = 100

# Estrategias unicas: selecao por roleta (Monte Carlo) e cruzamento de um
# ponto no centro. Exibidas no painel.
SELECTION = "roleta"
CROSSOVER = "um_ponto_centro"

CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "checkpoints")
