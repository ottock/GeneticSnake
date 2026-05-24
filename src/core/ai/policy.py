import numpy as np

from . import config


_INIT_PRIOR = np.array([
    -3.0,  # dies          -> evitar morte
    -1.5,  # 1/wall_dist   -> evitar parede (forte)
    -0.5,  # 1/body_dist   -> evitar corpo
     1.0,  # food_in_ray   -> comida na linha de visao (<=8 quadrados)
     1.5,  # food_align    -> alinhar com a comida (so se visivel)
     1.0,  # food_closer   -> chegar mais perto (so se visivel)
    -0.3,  # body_density  -> evitar areas cheias
     0.5,  # explore_centro-> procurar pelo mapa quando nao ve comida
     0.0,  # bias
], dtype=np.float32)

# 0.0 = puramente aleatorio (evolucao demora pra arrancar)
# 1.0 = prior forte (geracao 1 ja joga bem)
# Em 0.5, a populacao inicial mantem diversidade (ruido std 0.6 ainda domina
# os pesos individuais), mas com inclinacao suficiente pra evitar suicidio.
_INIT_STRENGTH = 0.5


def random_chromosome():
    noise = np.random.randn(config.CHROMOSOME_SIZE).astype(np.float32) * 0.6
    return _INIT_PRIOR * _INIT_STRENGTH + noise


def _scan_ray(start, direction, blocked, max_range):
    """Casts a ray up to max_range cells. Returns (wall_dist, body_dist), each
    a 1..max_range distance or None if not detected within range."""
    x, y = start
    dx, dy = direction
    wall_dist = None
    body_dist = None
    for dist in range(1, max_range + 1):
        x += dx
        y += dy
        if x < 0 or x >= config.GRID_W or y < 0 or y >= config.GRID_H:
            wall_dist = dist
            break
        if body_dist is None and (x, y) in blocked:
            body_dist = dist
    return wall_dist, body_dist


def _food_in_line(start, direction, food, max_range):
    if food is None:
        return False
    fx, fy = food
    sx, sy = start
    dx, dy = direction
    if dx == 0 and dy == 0:
        return False
    if dx == 0:
        if fx != sx:
            return False
        diff = fy - sy
        return diff != 0 and (diff * dy) > 0 and abs(diff) <= max_range
    if dy == 0:
        if fy != sy:
            return False
        diff = fx - sx
        return diff != 0 and (diff * dx) > 0 and abs(diff) <= max_range
    return False


def features_for_action(snake, new_direction):
    dx, dy = config.MOVES[new_direction]
    hx, hy = snake.body[0]
    nx, ny = hx + dx, hy + dy

    food = snake.food
    body_no_tail = set(snake.body)
    body_no_tail.discard(snake.body[-1])

    out_of_bounds = (nx < 0 or nx >= config.GRID_W
                     or ny < 0 or ny >= config.GRID_H)
    dies = 1.0 if out_of_bounds or (nx, ny) in body_no_tail else 0.0

    if out_of_bounds:
        wall_dist_inv = 1.0
        body_dist_inv = 0.0
    else:
        wall_dist, body_dist = _scan_ray(
            (nx, ny), (dx, dy), body_no_tail, config.VISION_RANGE)
        wall_dist_inv = 1.0 / wall_dist if wall_dist is not None else 0.0
        body_dist_inv = 1.0 / body_dist if body_dist is not None else 0.0

    food_in_ray = 0.0
    food_align = 0.0
    food_closer = 0.0
    food_visivel = False
    if food is not None:
        fx, fy = food
        # A cobra so "ve" a comida se estiver dentro de VISION_RANGE quadrados
        # (distancia de Chebyshev a partir da cabeca atual).
        food_visivel = max(abs(fx - hx),
                           abs(fy - hy)) <= config.VISION_RANGE
        if food_visivel:
            if not out_of_bounds and _food_in_line(
                    (nx, ny), (dx, dy), food, config.VISION_RANGE):
                food_in_ray = 1.0
            vx, vy = fx - hx, fy - hy
            norm = (vx * vx + vy * vy) ** 0.5
            if norm > 0:
                food_align = (vx * dx + vy * dy) / norm
            cur_d = abs(fx - hx) + abs(fy - hy)
            new_d = abs(fx - nx) + abs(fy - ny)
            food_closer = 1.0 if new_d < cur_d else 0.0

    body_density = 0.0
    if not out_of_bounds:
        count = 0
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if (nx + ox, ny + oy) in snake.body_set:
                    count += 1
        body_density = count / 9.0

    # Quando nao ha comida visivel, premia mover-se em direcao ao centro do
    # mapa (procura pelo mapa). Quando ha comida visivel, esse sinal e' zero.
    explore_centro = 0.0
    if not out_of_bounds and not food_visivel:
        cx = (config.GRID_W - 1) / 2.0
        cy = (config.GRID_H - 1) / 2.0
        vx, vy = cx - hx, cy - hy
        norm = (vx * vx + vy * vy) ** 0.5
        if norm > 0:
            explore_centro = (vx * dx + vy * dy) / norm

    return np.array([
        dies,
        wall_dist_inv,
        body_dist_inv,
        food_in_ray,
        food_align,
        food_closer,
        body_density,
        explore_centro,
        1.0,
    ], dtype=np.float32)


def choose_action(chromosome, snake):
    candidates = (
        config.LEFT_TURN[snake.direction],
        snake.direction,
        config.RIGHT_TURN[snake.direction],
    )
    best_idx = 0
    best_score = -float("inf")
    for i, new_dir in enumerate(candidates):
        feats = features_for_action(snake, new_dir)
        score = float(np.dot(chromosome, feats))
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx
