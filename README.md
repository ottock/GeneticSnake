# GeneticSnake

Jogo da cobrinha jogado por uma pequena rede neural feed-forward cujos pesos são
evoluídos com um algoritmo genético. Construído com Python, NumPy e pygame.

## Estrutura do Projeto

```
src/
├── core/                 # backend (Inglês)
│   ├── ai/               # GA, rede neural, configuração, fitness
│   └── models/           # estado do jogo da cobrinha, loop do treinador
└── presentation/         # frontend (Interface em Português)
    └── gui/              # app pygame, layout, renderizador, paleta
scripts/
└── createVenv.bat        # Script para criar venv no Windows
requirements.txt
```

## Requisitos

- Python 3.10+
- pip
- (Windows) `cmd` ou PowerShell

## Configuração

### Windows (script único)

A partir da raiz do projeto:

```bat
scripts\createVenv.bat
```

O script cria `.venv/`, ativa o ambiente virtual e instala as dependências do
`requirements.txt`.

### Windows (manual)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux / macOS (manual)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executando

Com o ambiente virtual ativo:

```bash
python src/main.py
```

## Controles

| Tecla          | Ação                                             |
| -------------- | ------------------------------------------------ |
| `TAB`          | Alterna renderização (desligado = treinamento mais rápido) |
| `ESPAÇO`       | Alterna limite de FPS                            |
| `CIMA` / `BAIXO` | Dobra / reduz pela metade o FPS alvo            |
| `ESC`          | Sair                                             |

## Configuração

Todos os hiperparâmetros do GA / rede estão em
[src/core/ai/config.py](src/core/ai/config.py):

- `POP_SIZE`, `ELITE_COUNT`, `TOURNAMENT_K`
- `MUTATION_RATE`, `MUTATION_STRENGTH`, `CROSSOVER_RATE`
- `SELECTION` — `"roulette"` ou `"tournament"`
- `CROSSOVER` — `"one_point"` ou `"uniform"`
- `HIDDEN1`, `HIDDEN2` — tamanhos das camadas ocultas
- `GRID_W`, `GRID_H` — tamanho do tabuleiro

## Checkpoints

O melhor genoma de cada geração é salvo em
`checkpoints/snake_best.npy`, e um CSV log de (geração, melhor_score,
melhor_fitness) é anexado a `checkpoints/snake_log.csv`. Ambos são ignorados
por git.
