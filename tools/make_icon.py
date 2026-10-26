#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисует иконку приложения: ночной роботизированный ГИГА-ПИСЮН из режима «Битва за Писюн».

Всё рисуется кодом (pygame), без внешних картинок. Запуск (из любой папки):

    pip install pygame
    python tools/make_icon.py

Результат (рядом с buildozer.spec, в корне проекта):
    icon.png      512x512  — обычная иконка (ночной город + робот)
    icon_fg.png   432x432  — адаптивная иконка, слой переднего плана (робот на прозрачном фоне)
    icon_bg.png   432x432  — адаптивная иконка, слой фона (ночное небо и город)
"""
import math
import os
import random
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

pygame.init()
pygame.display.set_mode((1, 1))

SHAPE = [
    ".XXX.",
    "XXXXX",
    ".XXX.",
    ".XXX.",
    ".XXX.",
    "XX.XX",
    "XX.XX",
]
BLACK = (20, 20, 30)
WHITE = (255, 255, 255)


# ---------------------------------------------------------------------------
# примитивы
# ---------------------------------------------------------------------------
def glow(surf, cx, cy, r, col, strength=1.0, power=1.7, steps=40):
    """Мягкое свечение: радиальный градиент по альфе, рисуется поверх обычным наложением."""
    r = int(r)
    g = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    for i in range(steps, 0, -1):
        k = i / steps
        a = int(255 * strength * (1.0 - k) ** power)
        pygame.draw.circle(g, (*col, max(0, min(255, a))), (r, r), max(1, int(r * k)))
    surf.blit(g, (int(cx - r), int(cy - r)))


def bar(scr, col, a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d * w / 2, dx / d * w / 2
    pygame.draw.polygon(scr, col, [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny),
                                   (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)])
    pygame.draw.circle(scr, col, (int(a[0]), int(a[1])), int(w / 2))
    pygame.draw.circle(scr, col, (int(b[0]), int(b[1])), int(w / 2))


def cell_colors(r, c):
    if r <= 1 and not (r == 1 and c in (0, 4)):
        return (232, 92, 152), (168, 48, 100), (255, 176, 210)       # розовая броня головы
    if r == 1:
        return (120, 130, 152), (74, 82, 102), (168, 178, 198)       # плечевые шарниры
    if r <= 4:
        return (104, 116, 142), (68, 76, 98), (152, 164, 190)        # стальной корпус
    return (84, 90, 112), (54, 58, 76), (126, 134, 156)              # силовые капсулы


# ---------------------------------------------------------------------------
# робот
# ---------------------------------------------------------------------------
def draw_robot(surf, cx, y0, c):
    """cx — центр по X, y0 — верх тела (голова), c — размер клетки в пикселях."""
    x0 = cx - 2.5 * c
    ow = max(2, int(c * 0.055))

    # плазменное пламя двигателей под ногами
    for sx in (-1.0 * c, 1.0 * c):
        bx, by = int(cx + sx), int(y0 + 7 * c - 0.04 * c)
        fl = int(0.85 * c)
        pygame.draw.polygon(surf, (255, 120, 40), [(bx - 0.4 * c, by), (bx + 0.4 * c, by), (bx, by + fl + 0.3 * c)])
        pygame.draw.polygon(surf, (255, 214, 110), [(bx - 0.23 * c, by), (bx + 0.23 * c, by), (bx, by + fl)])
        pygame.draw.polygon(surf, (255, 255, 230), [(bx - 0.09 * c, by), (bx + 0.09 * c, by), (bx, by + fl * 0.5)])

    # клетки корпуса
    for r, row in enumerate(SHAPE):
        for k, ch in enumerate(row):
            if ch != "X":
                continue
            base, dark, hi = cell_colors(r, k)
            x, y = int(x0 + k * c), int(y0 + r * c)
            s = int(c) + 1
            pygame.draw.rect(surf, base, (x, y, s, s))
            pygame.draw.rect(surf, hi, (x, y, s, max(2, int(0.11 * c))))
            pygame.draw.rect(surf, dark, (x, y + s - int(0.19 * c), s, int(0.19 * c)))
            pygame.draw.rect(surf, dark, (x, y, max(2, int(0.08 * c)), s))
            for (ax, ay) in ((0.17, 0.17), (0.83, 0.17), (0.17, 0.78), (0.83, 0.78)):
                pygame.draw.circle(surf, hi, (int(x + ax * c), int(y + ay * c)), max(1, int(0.055 * c)))
            if r == 1 and k in (0, 4):                                   # плечевые шарниры
                m = (int(x + c / 2), int(y + c / 2))
                pygame.draw.circle(surf, dark, m, int(0.31 * c))
                pygame.draw.circle(surf, (176, 186, 206), m, int(0.19 * c))
                pygame.draw.circle(surf, dark, m, int(0.19 * c), ow)
            if r == 4 and 1 <= k <= 3:                                   # предупреждающая полоса на поясе
                surf.set_clip(pygame.Rect(x, y, s, s))
                kk = -c
                while kk < c:
                    pygame.draw.polygon(surf, (240, 200, 40), [
                        (x + kk, y + c - 0.22 * c), (x + kk + 0.19 * c, y + c - 0.22 * c),
                        (x + kk + 0.39 * c, y + c - 0.03 * c), (x + kk + 0.19 * c, y + c - 0.03 * c)])
                    kk += 0.33 * c
                surf.set_clip(None)
            if r == 6 and k in (0, 1, 3, 4):                             # сопла-ступни
                pygame.draw.ellipse(surf, (36, 38, 50), (x + 0.17 * c, y + c - 0.33 * c, 0.66 * c, 0.28 * c))
            pygame.draw.rect(surf, BLACK, (x, y, s, s), ow)

    # визор
    vis = pygame.Rect(int(x0 + 1.1 * c), int(y0 + 1.22 * c), int(2.8 * c), int(0.62 * c))
    pygame.draw.rect(surf, (22, 24, 36), vis, border_radius=int(0.11 * c))
    pygame.draw.rect(surf, BLACK, vis, ow, border_radius=int(0.11 * c))

    # антенна
    pygame.draw.line(surf, (150, 156, 170), (int(cx), int(y0)), (int(cx), int(y0 - 0.5 * c)), max(3, int(0.08 * c)))
    glow(surf, cx, y0 - 0.55 * c, 0.5 * c, (255, 60, 50), 0.9)
    pygame.draw.circle(surf, (255, 80, 70), (int(cx), int(y0 - 0.55 * c)), int(0.14 * c))

    # реактор в груди
    ry = int(y0 + 3.5 * c)
    pygame.draw.circle(surf, (30, 32, 44), (int(cx), ry), int(0.44 * c))
    pygame.draw.circle(surf, BLACK, (int(cx), ry), int(0.44 * c), ow)
    glow(surf, cx, ry, 1.05 * c, (255, 140, 50), 0.75)
    pygame.draw.circle(surf, (255, 170, 80), (int(cx), ry), int(0.3 * c))
    pygame.draw.circle(surf, (255, 245, 210), (int(cx), ry), int(0.14 * c))

    # вентиляция груди
    for sg in (-1, 1):
        for j in range(3):
            yy = y0 + 2 * c + 0.28 * c + j * 0.22 * c
            pygame.draw.line(surf, (40, 44, 58), (cx + sg * 0.83 * c - 0.22 * c, yy),
                             (cx + sg * 0.83 * c + 0.22 * c, yy), max(2, int(0.055 * c)))

    # руки: плечо -> локоть -> клешня
    for sg in (-1, 1):
        S = (cx + sg * 2.0 * c, y0 + 1.5 * c)
        E = (cx + sg * 3.2 * c, y0 + 3.0 * c)
        T = (cx + sg * 2.95 * c, y0 + 4.65 * c)
        bar(surf, BLACK, S, E, 0.84 * c)
        bar(surf, (112, 122, 146), S, E, 0.61 * c)
        bar(surf, (176, 186, 206), (S[0] - 0.05 * c, S[1] - 0.08 * c), (E[0] - 0.05 * c, E[1] - 0.08 * c), 0.17 * c)
        bar(surf, BLACK, E, T, 0.72 * c)
        bar(surf, (112, 122, 146), E, T, 0.5 * c)
        for P, rr in ((S, 0.5 * c), (E, 0.42 * c)):
            pygame.draw.circle(surf, BLACK, (int(P[0]), int(P[1])), int(rr + ow))
            pygame.draw.circle(surf, (96, 104, 128), (int(P[0]), int(P[1])), int(rr))
            pygame.draw.circle(surf, (186, 194, 212), (int(P[0]), int(P[1])), int(rr / 3))
        th = math.atan2(T[1] - E[1], T[0] - E[0])
        for sgn in (-1, 1):                                              # клешня
            ang = th + sgn * 0.62
            ar = (math.cos(ang), math.sin(ang))
            ap = (-ar[1], ar[0])
            pts = [(T[0] + ap[0] * sgn * 0.25 * c, T[1] + ap[1] * sgn * 0.25 * c),
                   (T[0] + ar[0] * 0.85 * c + ap[0] * sgn * 0.36 * c, T[1] + ar[1] * 0.85 * c + ap[1] * sgn * 0.36 * c),
                   (T[0] + ar[0] * 1.55 * c, T[1] + ar[1] * 1.55 * c),
                   (T[0] + ar[0] * 0.9 * c - ap[0] * sgn * 0.11 * c, T[1] + ar[1] * 0.9 * c - ap[1] * sgn * 0.11 * c),
                   (T[0] - ap[0] * sgn * 0.17 * c, T[1] - ap[1] * sgn * 0.17 * c)]
            pygame.draw.polygon(surf, BLACK, pts)
            inner = [(T[0] + (px - T[0]) * 0.8, T[1] + (py - T[1]) * 0.8) for px, py in pts]
            pygame.draw.polygon(surf, (255, 110, 90), inner)
        pygame.draw.circle(surf, BLACK, (int(T[0]), int(T[1])), int(0.36 * c))
        pygame.draw.circle(surf, (255, 110, 90), (int(T[0]), int(T[1])), int(0.28 * c))

    # красные глаза поверх визора, со свечением
    ey = y0 + 1.5 * c
    k = c / 36.0
    for sg in (-1, 1):
        ex = cx + sg * 30 * k
        glow(surf, ex - sg * 4 * k, ey, 1.35 * c, (255, 50, 40), 0.95)
        pts = [(ex - sg * 20 * k, ey - 8 * k), (ex + sg * 10 * k, ey - 1 * k),
               (ex + sg * 10 * k, ey + 7 * k), (ex - sg * 20 * k, ey + 3 * k)]
        pygame.draw.polygon(surf, (255, 48, 36), pts)
        pygame.draw.polygon(surf, (255, 236, 220), [
            (ex - sg * 12 * k, ey - 3 * k), (ex + sg * 4 * k, ey), (ex + sg * 4 * k, ey + 3 * k), (ex - sg * 12 * k, ey + 1 * k)])


# ---------------------------------------------------------------------------
# ночной город
# ---------------------------------------------------------------------------
def night_bg(S, with_ground=True):
    surf = pygame.Surface((S, S))
    top, bot = (4, 6, 26), (40, 34, 92)
    for y in range(S):
        t = y / S
        surf.fill(tuple(int(top[i] + (bot[i] - top[i]) * (t ** 1.15)) for i in range(3)), (0, y, S, 1))
    rnd = random.Random(11)
    for _ in range(int(S * 0.11)):                                       # звёзды
        x, y = rnd.randrange(S), rnd.randrange(int(S * 0.62))
        col = rnd.choice(((255, 255, 255), (200, 212, 255), (255, 240, 200)))
        sz = max(1, int(S * (0.004 if rnd.random() < 0.8 else 0.008)))
        pygame.draw.rect(surf, col, (x, y, sz, sz))
    # луна
    mx, my, mr = int(S * 0.83), int(S * 0.17), int(S * 0.085)
    glow(surf, mx, my, mr * 3.2, (150, 160, 255), 0.35)
    pygame.draw.circle(surf, (232, 234, 210), (mx, my), mr)
    pygame.draw.circle(surf, (246, 246, 226), (mx - mr // 8, my - mr // 8), int(mr * 0.86))
    for (dx, dy, rr) in ((-0.35, 0.25, 0.18), (0.3, -0.2, 0.12), (0.4, 0.4, 0.14)):
        pygame.draw.circle(surf, (214, 218, 192), (int(mx + dx * mr), int(my + dy * mr)), int(rr * mr))
    # дальний ряд домов и ближний ряд
    for layer, (col, win, hmin, hmax, step) in enumerate((
            ((18, 24, 64), (60, 70, 130), 0.20, 0.42, 0.11),
            ((10, 14, 40), (255, 214, 120), 0.12, 0.30, 0.095))):
        x = -0.02 * S if layer == 0 else 0.03 * S
        while x < S:
            w = S * rnd.uniform(step * 0.8, step * 1.25)
            h = S * rnd.uniform(hmin, hmax)
            gy = S * (0.93 if with_ground else 1.0)
            pygame.draw.rect(surf, col, (int(x), int(gy - h), int(w) + 1, int(h) + 2))
            ws = max(2, int(S * 0.016))
            yy = gy - h + S * 0.02
            while yy < gy - S * 0.03:
                xx = x + S * 0.012
                while xx < x + w - ws * 2:
                    if rnd.random() < (0.55 if layer else 0.25):
                        pygame.draw.rect(surf, win, (int(xx), int(yy), ws, int(ws * 1.3)))
                    xx += ws * 2.2
                yy += ws * 2.6
            x += w + S * rnd.uniform(0.0, 0.015)
    if with_ground:
        pygame.draw.rect(surf, (28, 24, 44), (0, int(S * 0.93), S, S - int(S * 0.93)))
        pygame.draw.rect(surf, (70, 62, 96), (0, int(S * 0.93), S, max(2, int(S * 0.006))))
    return surf


def finish(surf, size, path):
    out = pygame.transform.smoothscale(surf, (size, size))
    pygame.image.save(out, path)
    print("записано:", path, out.get_size())


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here) if os.path.basename(here) == "tools" else here
    if len(sys.argv) > 1:
        root = sys.argv[1]

    # --- обычная иконка 512x512 (рисуем в 1024 и сжимаем — получается сглаженно)
    S = 1024
    c = 100
    surf = night_bg(S).convert_alpha()
    y0 = int(S / 2 - 3.675 * c)
    glow(surf, S / 2, y0 + 3.6 * c, 0.62 * S, (255, 60, 40), 0.42, 1.5)
    draw_robot(surf, S / 2, y0, c)
    finish(surf, 512, os.path.join(root, "icon.png"))

    # --- адаптивная иконка: два слоя 432x432 (рисуем в 1296 и сжимаем)
    S = 1296
    c = 96
    y0 = int(S / 2 - 3.675 * c)
    fg = pygame.Surface((S, S), pygame.SRCALPHA)
    glow(fg, S / 2, y0 + 3.6 * c, 0.46 * S, (255, 60, 40), 0.5, 1.5)
    draw_robot(fg, S / 2, y0, c)
    finish(fg, 432, os.path.join(root, "icon_fg.png"))
    finish(night_bg(S, with_ground=False), 432, os.path.join(root, "icon_bg.png"))


if __name__ == "__main__":
    main()
