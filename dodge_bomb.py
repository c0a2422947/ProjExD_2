import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    gg_img = pg.Surface((WIDTH, HEIGHT))
    gg_img.fill((0, 0, 0))
    pg.Rect(gg_img.get_rect())
    gg_img.set_alpha(200)
    fonto = pg.font.Font(None, 50)
    txt = fonto.render("GAME OVER", True, (255, 255, 255))
    gg_img.blit(txt, [WIDTH / 2 - 100, HEIGHT / 2])
    kk2_img = pg.image.load("fig/8.png")
    kk2_rct = kk2_img.get_rect()
    kk2_rct.center = WIDTH / 2 + 150, HEIGHT / 2
    gg_img.blit(kk2_img, kk2_rct)
    kk2_rct.center = WIDTH / 2 - 150, HEIGHT / 2
    gg_img.blit(kk2_img, kk2_rct)
    screen.blit(gg_img, [0, 0])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = 5
    bb_imgs, bb_accs = init_bb_imgs()
    DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(vx, vy)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if bb_img.get_width() != bb_rct.width:
            bb_rct.width = bb_img.get_rect().width
            bb_rct.height = bb_img.get_rect().height
        if check_bound(bb_rct) == (False, True):
            vx *= -1
        elif check_bound(bb_rct) == (True, False):
            vy *= -1

        if check_bound(kk_rct) != (True, True):
            kk_rct.center = 300, 200

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
