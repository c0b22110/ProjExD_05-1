import sys
import random
import pygame as pg
from pygame.math import Vector2


class Score:
    """
    coinを取ったときscoreが上がる(10点)
    """

    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.score = 100
        self.img = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.img.get_rect()
        self.rect.center = 100, 40

    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.img = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.img, self.rect)

    def get_score(self):  # int型のスコアを返す関数
        return int(self.score)


class Coin:
    """
    coinに関するclass
    """

    def __init__(self, screen_width, screen_height):
        self.image = pg.image.load("ex05/fig/coin.png")
        self.images = pg.transform.scale(self.image, (40, 40))
        self.rect = self.images.get_rect()
        self.rect.x = screen_width - self.rect.width
        self.rect.y = random.randint(0, screen_height - self.rect.height)

    def update(self, screen: pg.Surface):
        if self.rect.x >= 0:
            self.rect.move_ip(-2, 0)
            screen.blit(self.images, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)


class Player:
    player_y = 400

    def __init__(self):
        self.image = pg.image.load("ex05/fig/danieru.png")  # 通常時の姿
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.invincible_image = pg.image.load("ex05/fig/supadanieru.png")  # 無敵時の姿
        self.invincible_image = pg.transform.flip(self.invincible_image, True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, Player.player_y)
        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        if self.invincible:
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image = pg.image.load("ex05/fig/danieru.png")  # 元の画像に戻す
                self.image = pg.transform.rotozoom(self.image, 0, 0.5)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.invincible_timer -= 1
                self.image = self.invincible_image

    def set_invincible(self):
        """
        無敵機能
        """
        if self.invincible_timer <= 0:
            self.invincible = True
            self.invincible_timer = 500
            self.image = self.invincible_image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pg.transform.flip(self.image, True, False)

    def jump(self):
        self.player_y_vel = -20  # ジャンプ時のY方向の速度を設定
        self.jumping = True  # ジャンプ中のフラグを立てる

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Power:
    """
    スコアが一定以上を越えればパワーアップする（見た目）
    """

    def __init__(self, score):
        self.score = score
        self.power = False
        self.da_img = pg.image.load("ex05/fig/danieru.png")
        self.da_img = pg.transform.rotozoom(self.da_img, 0, 0.5)
        self.po_img = pg.image.load("ex05/fig/power.png")
        self.po_imgs = pg.transform.rotozoom(
            pg.transform.flip(self.po_img, True, False), 0, 0.5
        )  # デフォルトのimage
        self.now_img = self.da_img  # 現在の状態

    def rct(self):
        return self.now_img

    def update(self):
        if self.score >= 50 and not self.power:  # スコアが５を超えたらパワーアップ
            self.power_up()
        if self.score == 4:  # パワーアップしたら音が鳴る
            self.sound()

    def power_up(self):  # パワーアップの状態
        self.power = True
        self.now_img = self.po_imgs

    def draw(self, screen, x, y):  # 現在の状態のプレイヤーを描写
        screen.blit(self.now_img, (x, y))

    def sound(self):
        pg.mixer.init()
        pg.mixer.music.load("ex05/fig/power.mp3")
        pg.mixer.music.play()  # パワーアップサウンド


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

    def check_collision(self, player_rect):
        if self.active:
            if player_rect.colliderect(self.rect):
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y])


def main():
    pg.init()
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.5)
    bg_imgs = [bg_img, pg.transform.flip(bg_img, True, False)] * 2

    game_over_font = pg.font.Font(None, 64)  # ゲームオーバーメッセージ用のフォント

    score = Score()
    coin = Coin(800, 600)

    player = Player()
    obstacle = Obstacle()

    font = pg.font.SysFont(None, 36)

    tmr = 0
    running = True

    power = Power(score.get_score())

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not player.jumping:
                    player.jump()  # ジャンプ処理
                elif event.key == pg.K_LSHIFT:
                    if score.get_score() >= 10:
                        player.set_invincible()
                        score.score_up(-10)  # スコアを10減らす

        # 以下、ゲームループ内の処理
        screen.blit(bg_img, (0, 0))
        player.update()
        obstacle.update()
        obstacle.check_collision(player.rect)  # 衝突判定
        coin.update(screen)
        score.update(screen)
        power.update()
        power.draw(screen, 200, player.rect.y)
        screen.blit(kk_img, (200, player.rect.y))

        if tmr % 550 == 0:
            coin = Coin(screen.get_width(), screen.get_height())

        if coin.check_collision(player.rect):  # コインとの衝突判定
            score.score_up(10)

        if player.invincible_timer > 0:  # 無敵時間のカウントダウン
            player.invincible_timer -= 1

        if not player.invincible and obstacle.active and player.rect.colliderect(
            obstacle.rect
        ):  # 無敵でなく、障害物に衝突した場合はゲームオーバー
            running = False

        tmr += 1

        pg.display.update()
        clock.tick(60)

    # ゲームオーバー処理（必要に応じて追加）

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
