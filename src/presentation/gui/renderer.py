"""Renderizacao: cobra a esquerda, painel informativo a direita.

O painel mostra:
  - estatisticas do individuo atual e da populacao
  - parametros do Algoritmo Genetico
  - os bits do cromossomo da cobra que esta sendo avaliada agora
"""

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


def _draw_panel_header(screen, fonts, inner_l, y):
    fbig, _, ftiny = fonts
    screen.blit(fbig.render("Genetic Snake", True, P.HEADER), (inner_l, y))
    y += 28
    screen.blit(ftiny.render("algoritmo genetico - roleta + cruzamento + mutacao",
                             True, P.TEXT_DIM), (inner_l, y))
    return y + 18


def _section(screen, fonts, inner_l, inner_r, y, title):
    _, _, ftiny = fonts
    y += 5
    pygame.draw.line(screen, P.DIVIDER, (inner_l, y), (inner_r, y))
    y += 5
    screen.blit(ftiny.render(title.upper(), True, P.ACCENT), (inner_l, y))
    return y + 14


def _draw_kv_pair(screen, fonts, x_a, x_b, y, label_a, val_a, label_b, val_b,
                  color_a, color_b):
    _, fmid, ftiny = fonts
    screen.blit(ftiny.render(label_a, True, P.TEXT_DIM), (x_a, y))
    screen.blit(fmid.render(str(val_a), True, color_a), (x_a, y + 12))
    screen.blit(ftiny.render(label_b, True, P.TEXT_DIM), (x_b, y))
    screen.blit(fmid.render(str(val_b), True, color_b), (x_b, y + 12))
    return y + 34


def _draw_individual(screen, fonts, inner_l, inner_r, col2, y, info):
    y = _section(screen, fonts, inner_l, inner_r, y, "Individuo atual")
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Geracao",   info['generation'],
                      "Individuo", f"{info['individual']}/{config.SOL_POR_POP}",
                      P.ACCENT, P.TEXT)
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Comidas", info['score'],
                      "Tamanho", info['length'],
                      P.TEXT, P.TEXT)
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Passos",   info['steps'],
                      "Aptidao",  f"{info['aptidao']:.0f}",
                      P.TEXT, P.TEXT)
    return y


def _draw_stats(screen, fonts, inner_l, inner_r, col2, y, info):
    _, fmid, ftiny = fonts
    y = _section(screen, fonts, inner_l, inner_r, y, "Estatisticas")
    screen.blit(ftiny.render("Melhor geracao", True, P.TEXT_DIM),
                (inner_l, y))
    screen.blit(fmid.render(str(info['best_ever_generation']),
                            True, P.ACCENT), (inner_l, y + 12))
    y += 34
    screen.blit(ftiny.render("Aptidao media", True, P.TEXT_DIM),
                (inner_l, y))
    screen.blit(fmid.render(f"{info['media_aptidao']:.0f}", True, P.TEXT),
                (inner_l, y + 12))
    return y + 34


def _draw_ga_params(screen, fonts, inner_l, inner_r, col2, y):
    y = _section(screen, fonts, inner_l, inner_r, y, "Parametros GA")
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Selecao",    config.SELECTION,
                      "Cruzamento", config.CROSSOVER,
                      P.TEXT, P.TEXT)
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Sol/pop",    config.SOL_POR_POP,
                      "Num pesos",  config.NUM_PESOS,
                      P.TEXT, P.TEXT)
    y = _draw_kv_pair(screen, fonts, inner_l, col2, y,
                      "Num mutacoes", config.NUM_MUTACOES,
                      "Num geracoes", config.NUM_GERACOES,
                      P.TEXT, P.TEXT)
    return y


def _draw_chromosome(screen, fonts, inner_l, inner_r, y, chromosome):
    """Mostra os bits do cromossomo da cobra atual com seus rotulos."""
    _, _, ftiny = fonts
    y = _section(screen, fonts, inner_l, inner_r, y,
                 f"Cromossomo ({config.CHROMOSOME_SIZE} bits)")
    if chromosome is None:
        screen.blit(ftiny.render("(sem cromossomo)", True, P.TEXT_DIM),
                    (inner_l, y))
        return y + 14
    val_x = inner_l + 130
    bar_x = inner_l + 180
    bar_w = inner_r - bar_x
    bar_h = 7
    row_h = 14
    max_abs = max(1e-6, float(max(abs(float(v)) for v in chromosome)))
    for i, value in enumerate(chromosome):
        v = float(value)
        label = config.FEATURE_LABELS[i]
        screen.blit(ftiny.render(f"b{i} {label}", True, P.TEXT),
                    (inner_l, y))
        num_color = P.BIT_POS if v >= 0 else P.BIT_NEG
        screen.blit(ftiny.render(f"{v:+.2f}", True, num_color),
                    (val_x, y))
        mid = bar_x + bar_w // 2
        pygame.draw.line(screen, P.DIVIDER,
                         (bar_x, y + row_h // 2),
                         (bar_x + bar_w, y + row_h // 2))
        pygame.draw.line(screen, P.TEXT_DIM,
                         (mid, y + row_h // 2 - 3),
                         (mid, y + row_h // 2 + 3))
        norm = v / max_abs
        bw = int(abs(norm) * (bar_w // 2 - 2))
        rx = mid if v >= 0 else mid - bw
        pygame.draw.rect(screen, num_color,
                         (rx, y + row_h // 2 - bar_h // 2, bw, bar_h))
        y += row_h + 2
    return y


def _draw_controls(screen, fonts, inner_l, inner_r, y, info):
    _, _, ftiny = fonts
    y = _section(screen, fonts, inner_l, inner_r, y, "Comandos")
    fps_label = (f"{info['fps_target']} fps"
                 if info['fps_cap'] else "ilimitado")
    hints = (
        ("[UP/DOWN]", f"velocidade  {fps_label}"),
        ("[SPACE]",   f"limite fps  {'on' if info['fps_cap'] else 'off'}"),
        ("[TAB]",     f"renderizar  {'on' if info['visualize'] else 'off'}"),
        ("[ESC]",     "sair"),
    )
    for key, desc in hints:
        screen.blit(ftiny.render(key, True, P.ACCENT), (inner_l, y))
        screen.blit(ftiny.render(desc, True, P.TEXT_DIM),
                    (inner_l + 88, y))
        y += 16
    return y


def draw_panel(screen, layout, fonts, info):
    x0 = layout.panel_x
    pad = 18
    inner_l = x0 + pad
    inner_r = x0 + layout.panel_w - pad
    col2 = inner_l + (inner_r - inner_l) // 2 + 6

    pygame.draw.rect(screen, P.PANEL_BG, (x0, 0, layout.panel_w, layout.win_h))

    y = 14
    y = _draw_panel_header(screen, fonts, inner_l, y)
    y = _draw_individual(screen, fonts, inner_l, inner_r, col2, y, info)
    y = _draw_stats(screen, fonts, inner_l, inner_r, col2, y, info)
    y = _draw_ga_params(screen, fonts, inner_l, inner_r, col2, y)
    y = _draw_chromosome(screen, fonts, inner_l, inner_r, y,
                         info.get("chromosome"))
    _draw_controls(screen, fonts, inner_l, inner_r, y, info)
