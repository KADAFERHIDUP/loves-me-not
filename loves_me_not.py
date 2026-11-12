"""Loves me, loves me not - pixel art dengan pygame.
Instalasi : pip install pygame
Kontrol   : klik / Spasi = cabut satu kelopak, R = ulang, Esc = keluar
"""
import math
import random
import sys

import pygame

W, H = 180, 240                 # resolusi internal (pixel art)
N_PETALS = 12
CX, CY = 90, 108                # pusat bunga
STEM_BOTTOM = (90, 208)
LOVES_COLOR = (255, 143, 192)   # #ff8fc0
NOT_COLOR = (169, 188, 255)     # #a9bcff
IDLE_COLOR = (192, 224, 36)

PETAL_FILL = (255, 250, 245)
PETAL_SHADE = (222, 214, 228)
PETAL_LINE = (120, 100, 140)
CENTER_DARK = (196, 120, 20)
CENTER_MID = (240, 176, 30)
CENTER_LIGHT = (255, 222, 90)
STEM_COLOR = (50, 140, 60)
STEM_DARK = (30, 95, 45)

pygame.init()
info = pygame.display.Info()
start_scale = max(1, int(min(info.current_w * 0.8 // W, info.current_h * 0.8 // H)))
screen = pygame.display.set_mode((W * start_scale, H * start_scale), pygame.RESIZABLE)
pygame.display.set_caption("Loves me, loves me not")
buf = pygame.Surface((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas,couriernew,monospace", 18, bold=True)
small_font = pygame.font.SysFont("consolas,couriernew,monospace", 12, bold=True)

# ---------- dekor statis ----------
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_background():
    bg = pygame.Surface((W, H))
    top, bottom = (8, 12, 58), (110, 70, 150)
    bands = 7
    for y in range(H):
        t = min(1.0, y / (H * 0.8))
        v = t * bands
        i = int(v)
        frac = v - i
        for x in range(W):
            k = i + (1 if frac > BAYER[y % 4][x % 4] / 16 else 0)
            bg.set_at((x, y), lerp(top, bottom, min(k, bands) / bands))
    # bukit
    for x in range(W):
        y1 = int(172 + 9 * math.sin(x * 0.035) + 5 * math.sin(x * 0.09 + 1))
        pygame.draw.line(bg, (28, 38, 110), (x, y1), (x, H))
        y2 = int(190 + 4 * math.sin(x * 0.06 + 2))
        pygame.draw.line(bg, (20, 70, 50), (x, y2), (x, H))
    # tanah
    pygame.draw.rect(bg, (30, 90, 40), (0, 200, W, H - 200))
    # bulan
    pygame.draw.circle(bg, (250, 240, 200), (148, 30), 11)
    pygame.draw.circle(bg, (224, 212, 170), (144, 27), 3)
    pygame.draw.circle(bg, (224, 212, 170), (151, 35), 2)
    return bg


random.seed(4)
BG = make_background()
STARS = [(random.randint(2, W - 2), random.randint(2, 120), random.random() * 6.28)
         for _ in range(45)]
GRASS = [(random.randint(0, W), random.randint(194, 232), random.randint(3, 9),
          random.choice([(60, 150, 60), (40, 120, 50), (90, 180, 70)]),
          random.random() * 6.28)
         for _ in range(140)]
random.seed()


# ---------- kelopak ----------
def petal_points(angle, length=26, width=9):
    """Titik-titik poligon satu kelopak (bentuk tetes) menghadap `angle`."""
    pts = []
    steps = 14
    for i in range(steps + 1):
        t = i / steps
        r = 7 + length * t
        w = width * math.sin(math.pi * t) * (1 - 0.35 * t)
        px = math.cos(angle) * r - math.sin(angle) * w
        py = math.sin(angle) * r + math.cos(angle) * w
        pts.append((CX + px, CY + py))
    for i in range(steps, -1, -1):
        t = i / steps
        r = 7 + length * t
        w = -width * math.sin(math.pi * t) * (1 - 0.35 * t)
        px = math.cos(angle) * r - math.sin(angle) * w
        py = math.sin(angle) * r + math.cos(angle) * w
        pts.append((CX + px, CY + py))
    return [(round(x), round(y)) for x, y in pts]


def draw_petal(surf, angle, offset=(0, 0), rot=0.0):
    pts = petal_points(angle + rot)
    if offset != (0, 0):
        pts = [(x + offset[0], y + offset[1]) for x, y in pts]
    pygame.draw.polygon(surf, PETAL_FILL, pts)
    # bayangan di satu sisi kelopak
    half = pts[len(pts) // 2:]
    shade = [((x + CX + offset[0]) // 2, (y + CY + offset[1]) // 2) for x, y in half]
    if len(half) > 2:
        pygame.draw.polygon(surf, PETAL_SHADE, half + shade[::-1])
    pygame.draw.polygon(surf, PETAL_LINE, pts, 1)


class FallingPetal:
    def __init__(self, angle):
        self.angle = angle
        self.x = 0.0
        self.y = 0.0
        self.vx = math.cos(angle) * 22 + random.uniform(-8, 8)
        self.vy = -18 + random.uniform(-6, 2)
        self.rot = 0.0
        self.spin = random.uniform(-3, 3)
        self.t = 0.0

    def update(self, dt):
        self.t += dt
        self.vy = min(self.vy + 60 * dt, 28)            # gravitasi + hambatan udara
        self.x += (self.vx + 10 * math.sin(self.t * 4)) * dt
        self.vx *= 0.985
        self.y += self.vy * dt
        self.rot += self.spin * dt

    def alive(self):
        return CY + self.y < H + 40

    def draw(self, surf):
        draw_petal(surf, self.angle, (round(self.x), round(self.y)), self.rot)


# ---------- state permainan ----------
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.n = random.randint(N_PETALS - 3, N_PETALS + 3)   # jumlah acak = hasil acak
        base = random.random() * math.tau
        self.petals = [base + i * math.tau / self.n for i in range(self.n)]
        self.falling = []
        self.plucked = 0
        self.message = "click to pluck"
        self.msg_color = IDLE_COLOR
        self.done = False
        self.pop = 0.0      # animasi teks membesar

    def pluck(self):
        if self.done or not self.petals:
            return
        # cabut kelopak yang paling dekat dengan arah kanan-atas (terasa natural)
        idx = min(range(len(self.petals)),
                  key=lambda i: abs(math.atan2(math.sin(self.petals[i] + 0.8),
                                               math.cos(self.petals[i] + 0.8))))
        angle = self.petals.pop(idx)
        self.falling.append(FallingPetal(angle))
        self.plucked += 1
        loves = self.plucked % 2 == 1
        self.message = "loves me" if loves else "loves me not"
        self.msg_color = LOVES_COLOR if loves else NOT_COLOR
        self.pop = 1.0
        if not self.petals:
            self.done = True
            self.message = "LOVES ME! <3" if loves else "loves me not..."

    def update(self, dt):
        for p in self.falling:
            p.update(dt)
        self.falling = [p for p in self.falling if p.alive()]
        self.pop = max(0.0, self.pop - dt * 3)


def draw_scene(game, t):
    buf.blit(BG, (0, 0))

    # bintang berkelip
    for x, y, ph in STARS:
        b = 0.5 + 0.5 * math.sin(t * 2 + ph)
        c = lerp((90, 90, 150), (255, 255, 230), b)
        buf.set_at((x, y), c)
        if b > 0.93:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                buf.set_at((x + dx, y + dy), lerp((90, 90, 150), c, 0.6))

    # batang + daun (bergoyang pelan)
    sway = math.sin(t * 1.3) * 1.5
    pts = []
    for i in range(21):
        k = i / 20
        x = STEM_BOTTOM[0] + sway * (1 - k) * k * 4 + math.sin(k * 3) * 2
        y = STEM_BOTTOM[1] + (CY - STEM_BOTTOM[1]) * k
        pts.append((round(x), round(y)))
    pygame.draw.lines(buf, STEM_DARK, False, [(x + 1, y) for x, y in pts], 2)
    pygame.draw.lines(buf, STEM_COLOR, False, pts, 2)
    for side, ly in ((-1, 170), (1, 152)):
        lx = STEM_BOTTOM[0] + 1
        leaf = [(lx, ly), (lx + side * 9, ly - 6), (lx + side * 17, ly - 4),
                (lx + side * 10, ly + 1)]
        pygame.draw.polygon(buf, STEM_COLOR, leaf)
        pygame.draw.line(buf, STEM_DARK, (lx, ly), (lx + side * 14, ly - 4))

    # rumput bergoyang
    for gx, gy, gh, gc, ph in GRASS:
        tip = gx + round(math.sin(t * 2 + ph) * 1.5)
        pygame.draw.line(buf, gc, (gx, gy), (tip, gy - gh))

    # kelopak yang masih menempel
    for a in game.petals:
        draw_petal(buf, a)

    # putik / pusat bunga
    pygame.draw.circle(buf, CENTER_DARK, (CX, CY), 9)
    pygame.draw.circle(buf, CENTER_MID, (CX, CY), 7)
    pygame.draw.circle(buf, CENTER_LIGHT, (CX - 2, CY - 2), 3)
    for i in range(10):
        a = i * math.tau / 10 + 0.3
        buf.set_at((round(CX + math.cos(a) * 5), round(CY + math.sin(a) * 5)), CENTER_DARK)

    # kelopak yang jatuh
    for p in game.falling:
        p.draw(buf)


def draw_text(surface, scale, game, t):
    sw, sh = surface.get_size()
    size = 1.0 + 0.35 * game.pop
    label = font.render(game.message, False, game.msg_color)
    label = pygame.transform.scale(
        label, (int(label.get_width() * scale / 2 * size), int(label.get_height() * scale / 2 * size)))
    shadow = font.render(game.message, False, (20, 10, 40))
    shadow = pygame.transform.scale(shadow, label.get_size())
    x = (sw - label.get_width()) // 2
    y = int(36 * scale) - label.get_height() // 2 + round(math.sin(t * 3) * scale)
    surface.blit(shadow, (x + scale, y + scale))
    surface.blit(label, (x, y))

    hint = "R = ulang   Esc = keluar" if game.done else f"kelopak tersisa: {len(game.petals)}"
    h = small_font.render(hint, False, (220, 210, 240))
    h = pygame.transform.scale(h, (int(h.get_width() * scale / 2), int(h.get_height() * scale / 2)))
    surface.blit(h, ((sw - h.get_width()) // 2, sh - h.get_height() - int(6 * scale)))


def main():
    global screen
    game = Game()
    t = 0.0
    while True:
        dt = clock.tick(60) / 1000
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    game.reset()
                if event.key == pygame.K_SPACE:
                    game.pluck()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.pluck()

        game.update(dt)
        draw_scene(game, t)

        # skala pixel-perfect ke ukuran jendela
        sw, sh = screen.get_size()
        scale = max(1, min(sw // W, sh // H))
        scaled = pygame.transform.scale(buf, (W * scale, H * scale))
        screen.fill((0, 0, 0))
        ox, oy = (sw - W * scale) // 2, (sh - H * scale) // 2
        screen.blit(scaled, (ox, oy))
        frame = screen.subsurface((ox, oy, W * scale, H * scale))
        draw_text(frame, scale, game, t)
        pygame.display.flip()


if __name__ == "__main__":
    main()
