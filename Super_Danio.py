import sys
import random
import pygame as pg
from pygame.math import Vector2


def main():
    global player_y  # player_y をグローバル変数として宣言
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.5)
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)] * 2
    
    game_over_font = pg.font.Font(None, 64)  # ゲームオーバーメッセージ用のフォント

    player_y = 400
    player_y_vel = 0
    jumping = False
    tmr = 0

    # 障害物クラス
    class Obstacle:
        def __init__(self):
            self.x = 800
            self.y = 480
            self.speed = 5
            self.active = True
            self.image = pg.image.load("ex05/fig/unnko.png")
            self.image = pg.transform.rotozoom(self.image, 0, 0.3)
            self.rect = self.image.get_rect()

        def update(self):
            self.x -= self.speed
            if self.x < -50:
                self.reset()

        def reset(self):
            self.x = 800
            self.active = True

        def check_collision(self):
            global player_y, running# player_y をグローバル変数として参照
            if self.active:
                # オブジェクトの中心座標と半径を計算
                obstacle_center = Vector2(self.rect.center)
                obstacle_radius = self.rect.width / 2

                kk_center = Vector2(200 + kk_img.get_width() / 2, player_y + kk_img.get_height() / 2)
                kk_radius = kk_img.get_width() / 2

                # 中心座標間の距離を計算
                distance = kk_center.distance_to(obstacle_center)

                # 距離が半径の和より小さい場合は衝突と判定
                if distance < obstacle_radius + kk_radius:
                    running = False

        def draw(self):
            screen.blit(self.image, [self.x, self.y])

    obstacle = Obstacle()
    running = True

    def draw_game_over():
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (300, 250))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            
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

        if running:
            obstacle.draw()
            screen.blit(kk_img, [200, player_y])
        else:
            draw_game_over()

        pg.display.update()
        tmr += 1
        clock.tick(100)

    # ゲームループ終了後にゲームオーバー画面を表示するなどの処理を追加することができます
    # 以下は単純にウィンドウを閉じるだけの処理です
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()