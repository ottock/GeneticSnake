"""Loop principal pygame: lê eventos, avança o Trainer, renderiza."""

import sys

try:
    import pygame
except ImportError:
    print("Faltando pygame. Rode: pip install pygame", file=sys.stderr)
    sys.exit(1)

from core.ai import config
from core.models.trainer import Trainer, save_best
from .layout import Layout, INIT_WIN_W, INIT_WIN_H
from . import palette as P
from .renderer import draw_game, draw_panel

FPS_DEFAULT = 12
FPS_MIN = 2
FPS_MAX = 240


def _make_fonts():
    return (
        pygame.font.SysFont("consolas", 24, bold=True),
        pygame.font.SysFont("consolas", 18, bold=True),
        pygame.font.SysFont("consolas", 12),
    )


def _build_info(trainer, visualize, fps_cap, fps_target):
    return {
        "generation":           trainer.generation,
        "individual":           trainer.idx + 1,
        "score":                trainer.snake.score,
        "length":               len(trainer.snake.body),
        "steps":                trainer.snake.steps,
        "aptidao":              trainer.current_aptidao(),
        "best_ever_score":      trainer.best_ever_score,
        "best_ever_generation": trainer.best_ever_generation,
        "media_aptidao":        trainer.media_aptidao,
        "visualize":            visualize,
        "fps_cap":              fps_cap,
        "fps_target":           fps_target,
        "chromosome":           trainer.snake.chromosome,
        "gen_best_history":     trainer.gen_best_history,
    }


def run():
    pygame.init()
    screen = pygame.display.set_mode((INIT_WIN_W, INIT_WIN_H), pygame.RESIZABLE)
    pygame.display.set_caption("GeneticSnake - Algoritmo Genetico (Roleta)")
    clock = pygame.time.Clock()
    fonts = _make_fonts()
    layout = Layout(INIT_WIN_W, INIT_WIN_H)

    trainer = Trainer()
    visualize = True
    fps_cap = True
    fps_target = FPS_DEFAULT
    running = True

    while running:
        sim_deadline = pygame.time.get_ticks() + (0 if fps_cap else 33)
        while True:
            snake_alive = trainer.step()
            if not snake_alive:
                if not trainer.next_individual():
                    summary = trainer.advance_generation()
                    if summary["best_chromosome"] is not None:
                        save_best(summary["best_chromosome"],
                                  summary["generation"],
                                  summary["best_score"],
                                  summary["best_aptidao"])
            if fps_cap or pygame.time.get_ticks() >= sim_deadline:
                break

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.VIDEORESIZE:
                layout = Layout(ev.w, ev.h)
                screen = pygame.display.set_mode(
                    (layout.win_w, layout.win_h), pygame.RESIZABLE)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_TAB:
                    visualize = not visualize
                elif ev.key == pygame.K_SPACE:
                    fps_cap = not fps_cap
                elif ev.key == pygame.K_UP:
                    fps_target = min(FPS_MAX, max(FPS_MIN, fps_target * 2))
                elif ev.key == pygame.K_DOWN:
                    fps_target = min(FPS_MAX,
                                     max(FPS_MIN, fps_target // 2 or FPS_MIN))

        screen.fill(P.BG)
        if visualize:
            draw_game(screen, layout, trainer.snake)
        draw_panel(screen, layout, fonts,
                   _build_info(trainer, visualize, fps_cap, fps_target))
        pygame.display.flip()
        if fps_cap and visualize:
            clock.tick(fps_target)

    pygame.quit()
