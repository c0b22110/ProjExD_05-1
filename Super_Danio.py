import sys
import pygame as pg


def main():
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.flip(kk_img,True,False)
    kk_imgs = pg.transform.rotozoom(kk_img,0,0.5)
    bg_imgs = [bg_img,pg.transform.flip(bg_img,True, False)]*2

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])

        for i in range(4):
            screen.blit(bg_imgs[i], [1600*i-x, 0])

        if tmr % 100 <= 50:
            screen.blit(kk_img, [300, 200])
        else:            
            screen.blit(kk_imgs,[300,200])
        pg.display.update()
        tmr += 1        
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()