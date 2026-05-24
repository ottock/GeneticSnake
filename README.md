# GeneticSnake

Jogo da cobrinha jogado por indivíduos cujo **cromossomo** (vetor de pesos) é
evoluído por **Algoritmo Genético** — método de otimização meta-heurístico
inspirado na seleção natural de Darwin (Holland, 1975). A seleção dos pais é
feita por **roleta** (Monte Carlo). Construído com Python, NumPy e pygame.

A cada passo, para cada ação possível (virar esquerda, seguir reto, virar
direita) são calculadas 8 features sobre o estado resultante (morre? distância
da parede, comida na linha de visão, alinhamento com a comida, etc.). O
cromossomo (vetor de 8 bits/pesos) pontua cada ação linearmente —
pontuação = `cromossomo · features`. A ação de maior pontuação é escolhida.

## Tela

- **Esquerda:** a cobra (indivíduo atual) jogando no tabuleiro.
- **Direita:** painel com estatísticas do indivíduo, parâmetros do GA e os
  bits do cromossomo da cobra atual.

## Estrutura do Algoritmo Genético

Seguindo o material da aula:

1. **População inicial** diversificada de cromossomos aleatórios.
2. **Avaliação** — cada indivíduo joga uma partida; sua pontuação reflete
   quão bem se saiu.
3. **Seleção por roleta** — cada indivíduo ocupa uma fatia da roleta
   proporcional à sua pontuação; gira-se a roleta para escolher pais.
4. **Cruzamento** — combina os cromossomos dos pais para gerar filhos
   (suporta cruzamento em um ponto e cruzamento uniforme).
5. **Mutação** — pequenas alterações aleatórias nos bits dos filhos.
6. Repete até atingir o critério de parada.

## Estrutura do Projeto

```
src/
├── core/                 # backend
│   ├── ai/               # GA (roleta), política, config, pontuação
│   └── models/           # estado do jogo, loop do treinador
└── presentation/         # frontend (em Português)
    └── gui/              # app pygame, layout, renderizador, paleta
scripts/
└── createVenv.bat        # cria venv no Windows
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

| Tecla            | Ação                                                       |
| ---------------- | ---------------------------------------------------------- |
| `TAB`            | Alterna renderização (desligado = treinamento mais rápido) |
| `ESPAÇO`         | Alterna limite de FPS                                      |
| `CIMA` / `BAIXO` | Dobra / reduz pela metade o FPS alvo                       |
| `ESC`            | Sair                                                       |

## Parâmetros do GA

Todos os parâmetros estão em [src/core/ai/config.py](src/core/ai/config.py):

- `POP_SIZE` — tamanho da população por geração
- `MUTATION_RATE` — probabilidade de cada bit do cromossomo sofrer mutação
- `MUTATION_STRENGTH` — intensidade da mutação
- `CROSSOVER_RATE` — probabilidade de cruzar (senão clona o pai 1)
- `CROSSOVER` — `"um_ponto"` ou `"uniforme"`
- `FEATURE_COUNT` — número de features (= tamanho do cromossomo)
- `GRID_W`, `GRID_H` — tamanho do tabuleiro

A seleção é fixada em **roleta**.

## Bits do cromossomo

O cromossomo tem 8 bits (pesos), um para cada feature do estado resultante
de uma ação:

| Bit | Rótulo          | Significado                                |
| --- | --------------- | ------------------------------------------ |
| b0  | `morre`         | 1 se a ação mata a cobra                   |
| b1  | `1/dist_parede` | inverso da distância à parede              |
| b2  | `1/dist_corpo`  | inverso da distância ao próprio corpo      |
| b3  | `comida_visao`  | 1 se a comida está na linha de visão       |
| b4  | `alinha_comida` | cosseno do ângulo com o vetor até a comida |
| b5  | `aproxima`      | 1 se a ação aproxima da comida             |
| b6  | `densidade`     | fração de células vizinhas ocupadas        |
| b7  | `bias`          | termo constante (offset)                   |

## Checkpoints

O melhor cromossomo de cada geração é salvo em `checkpoints/snake_best.npy`,
e um CSV log de (geração, melhor_comidas, melhor_pontuacao) é anexado a
`checkpoints/snake_log.csv`. Ambos são ignorados por git.

## Referência

Material base: *Aula Algoritmos Genéticos* — Prof. Carlos Menezes,
disciplina de Inteligência Artificial.
