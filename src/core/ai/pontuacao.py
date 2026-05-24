def pontuacao(steps, score):
    """Pontuacao do individuo.

    - Comer fruta vale muito (1000 por unidade).
    - Sobreviver mais passos da um pequeno bonus (1 por passo), garantindo
      sinal positivo mesmo nas geracoes iniciais em que poucas cobras comem.
    - Sempre nao-negativa, mantendo a roleta proporcional bem definida.
    """
    return score * 1000.0 + steps
