def pontuacao(steps, score):
    """Pontuacao do individuo: recompensa comida e penaliza passos perdidos."""
    return score * 10000.0 - steps * 0.1
