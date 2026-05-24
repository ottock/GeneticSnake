"""Calculo de layout para janela redimensionavel.

Layout: cobra no canto esquerdo, painel de informacoes na direita.
"""

from core.ai import config

INIT_WIN_W = 1240
INIT_WIN_H = 660
MIN_WIN_W = 800
MIN_WIN_H = 480
MIN_PANEL_W = 340
MAX_PANEL_W = 520


class Layout:
    def __init__(self, win_w, win_h):
        self.win_w = max(MIN_WIN_W, win_w)
        self.win_h = max(MIN_WIN_H, win_h)
        self.panel_w = max(MIN_PANEL_W,
                           min(MAX_PANEL_W, int(self.win_w * 0.38)))
        area_w = self.win_w - self.panel_w
        area_h = self.win_h
        self.cell = max(8, min(area_w // config.GRID_W,
                               area_h // config.GRID_H))
        self.game_w = self.cell * config.GRID_W
        self.game_h = self.cell * config.GRID_H
        self.game_x = (area_w - self.game_w) // 2
        self.game_y = (self.win_h - self.game_h) // 2
        self.panel_x = self.win_w - self.panel_w
