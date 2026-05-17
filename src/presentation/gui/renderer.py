import pygame

from core.ai import config
from . import palette as P


def draw_game(screen, layout, snake):
    gx, gy, cell = layout.game_x, layout.game_y, layout.cell
    pygame.draw.rect(screen, P.BG, (gx, gy, layout.game_w, layout.game_h))
    for i in range(config.GRID_W + 1):
        pygame.draw.line(screen, P.GRID_COLOR,
                         (gx + i * cell, gy),
                         (gx + i * cell, gy + layout.game_h))
    for j in range(config.GRID_H + 1):
        pygame.draw.line(screen, P.GRID_COLOR,
                         (gx, gy + j * cell),
                         (gx + layout.game_w, gy + j * cell))
    if snake.food is not None:
        fx, fy = snake.food
        pad = max(2, cell // 6)
        pygame.draw.rect(screen, P.FOOD_COLOR,
                         (gx + fx * cell + pad, gy + fy * cell + pad,
                          cell - 2 * pad, cell - 2 * pad),
                         border_radius=max(2, cell // 5))
    pad = max(1, cell // 10)
    for i, (bx, by) in enumerate(snake.body):
        color = P.SNAKE_HEAD if i == 0 else P.SNAKE_BODY
        pygame.draw.rect(screen, color,
                         (gx + bx * cell + pad, gy + by * cell + pad,
                          cell - 2 * pad, cell - 2 * pad),
                         border_radius=max(2, cell // 6))


def draw_panel(screen, layout, fonts, info):
    fbig, fmid, ftiny = fonts
    x0 = layout.panel_x
    pad = 18
    inner_l = x0 + pad
    inner_r = x0 + layout.panel_w - pad
    col2 = inner_l + (inner_r - inner_l) // 2 + 6

    pygame.draw.rect(screen, P.PANEL_BG, (x0, 0, layout.panel_w, layout.win_h))

    y = 16
    screen.blit(fbig.render("Genetic Snake", True, P.HEADER), (inner_l, y))
    y += 30
    screen.blit(ftiny.render("rede neural + algoritmo genetico",
                             True, P.TEXT_DIM), (inner_l, y))
    y += 20

    def section(title):
        nonlocal y
        y += 6
        pygame.draw.line(screen, P.DIVIDER, (inner_l, y), (inner_r, y))
        y += 6
        screen.blit(ftiny.render(title.upper(), True, P.ACCENT), (inner_l, y))
        y += 18

    def cell_kv(x, label, value, color):
        screen.blit(ftiny.render(label, True, P.TEXT_DIM), (x, y))
        v = fmid.render(str(value), True, color)
        screen.blit(v, (x, y + 14))

    def row_pair(label_a, val_a, label_b, val_b,
                 color_a=P.TEXT, color_b=P.TEXT):
        nonlocal y
        cell_kv(inner_l, label_a, val_a, color_a)
        cell_kv(col2,    label_b, val_b, color_b)
        y += 40

    # ---------- INDIVIDUO ATUAL ----------
    section("Individuo atual")
    row_pair("Geracao", info['generation'],
             "Cobra",   f"{info['individual']}/{config.POP_SIZE}",
             color_a=P.ACCENT)
    row_pair("Score",   info['score'],
             "Tamanho", info['length'])
    row_pair("Passos",  info['steps'],
             "Fitness", f"{info['fitness']:.0f}")

    # ---------- ESTATISTICAS ----------
    section("Estatisticas")
    row_pair("Melhor gen",   info['best_ever_generation'],
             "Melhor score", info['best_ever_score'],
             color_a=P.ACCENT, color_b=P.ACCENT)
    row_pair("Fitness medio", f"{info['avg_fitness']:.0f}",
             "Restantes",     info['remaining'])

    # ---------- PARAMETROS GA (Aula slides 8/10/11) ----------
    section("Parametros GA")
    row_pair("Selecao",    config.SELECTION,
             "Cruzamento", config.CROSSOVER)
    row_pair("Pop",     config.POP_SIZE,
             "Elite",   config.ELITE_COUNT)
    row_pair("Mutacao", f"{int(config.MUTATION_RATE * 100)}%",
             "Cross %", f"{int(config.CROSSOVER_RATE * 100)}%")

    # ---------- RODAPE ----------
    fps_label = (f"{info['fps_target']} fps"
                 if info['fps_cap'] else "ilimitado")
    hints = [
        ("[UP/DOWN]", f"velocidade  {fps_label}"),
        ("[SPACE]",   f"limite fps  {'on' if info['fps_cap'] else 'off'}"),
        ("[TAB]",     f"renderizar  {'on' if info['visualize'] else 'off'}"),
        ("[ESC]",     "sair"),
    ]
    hy = layout.win_h - 18 * len(hints) - 10
    for key, desc in hints:
        screen.blit(ftiny.render(key, True, P.ACCENT), (inner_l, hy))
        screen.blit(ftiny.render(desc, True, P.TEXT_DIM),
                    (inner_l + 92, hy))
        hy += 18
