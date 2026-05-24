def fitness_value(steps, score):
    if score == 0:
        return steps * 0.5
    base = steps + (2.0 ** min(score, 10)) + (score ** 2.1) * 500.0
    penalty = (steps ** 1.3) * (score ** 1.2) * 0.25
    return max(0.0, base - penalty)