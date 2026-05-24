"""APTIDAO

O valor de aptidao que o algoritmo genetico fornece e' o unico feedback que o
mecanismo obtem para guia-lo em direcao a uma solucao.
"""


def aptidao(steps, score):
    """Aptidao do individuo.

    - Comer fruta vale muito (1000 por unidade).
    - Sobreviver mais passos da um pequeno bonus (1 por passo), garantindo
      sinal positivo mesmo nas geracoes iniciais em que poucas cobras comem.
    - Sempre nao-negativa, mantendo as fatias da roleta bem definidas.
    """
    return score * 1000.0 + steps
