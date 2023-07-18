import sys
import random
import pygame as pg


def main():
    global player_y  # player_y をグローバル変数として宣言
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.5)
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)] * 2

    player_y = 400
    player_y_vel = 0
    jumping = False
    tmr = 0

    # 障害物クラス
    class Obstacle:
        def __init__(self):
            self.x = 800
            self.y = 400
            self.speed = 5
            self.active = True
            self.image = pg.image.load("ex05/fig/unnko.png")

        def update(self):
            self.x -= self.speed
            if self.x < -50:
                self.reset()

        def reset(self):
            self.x = 800
            self.active = True

        def check_collision(self):
            global player_y  # player_y をグローバル変数として参照
            if self.active and abs(player_y - self.y) < 50:
                player_y = 400
                player_y_vel = 0
                self.active = False

        def draw(self):
            screen.blit(self.image, [self.x, self.y])

    obstacle = Obstacle()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not jumping:
                    player_y_vel = -15
                    jumping = True

        x = tmr % 3200
        screen.blit(bg_img, [x, 0])

        if jumping:
            player_y_vel += 1
            player_y += player_y_vel
            if player_y >= 400:
                player_y = 400
                player_y_vel = 0
                jumping = False

        for i in range(4):
            screen.blit(bg_imgs[i], [1600 * i - x, 0])

        obstacle.update()
        obstacle.check_collision()
        obstacle.draw()

        screen.blit(kk_img, [200, player_y])
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()