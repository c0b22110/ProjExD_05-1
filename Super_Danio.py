import sys
import pygame as pg
import random

class Score:
    """
    coinを取ったときscoreが上がる(10点)
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.score = 0
        self.img = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.img.get_rect()
        self.rect.center = 100, 40
    
    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.img = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.img, self.rect)

    def get_score(self): # int型のスコアを返す関数
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
        # player_center_x = player_rect.centerx
        # player_center_y = player_rect.centery
        # coin_center_x = self.rect.centerx
        # coin_center_y = self.rect.centery
        # distance_x = abs(player_center_x - coin_center_x)
        # distance_y = abs(player_center_y - coin_center_y)
        # max_radius = max(player_rect.width, player_rect.height) // 2
        # coin_radius = max(self.rect.width, self.rect.height) // 2
        # if distance_x < max_radius + coin_radius and distance_y < max_radius + coin_radius:
        #     return True
        # return False
        return self.rect.colliderect(player_rect)
"""
score,enemy
"""

class Player:  #プレイヤークラス
    player_y = 400
    def __init__(self):
        self.image = pg.image.load("ex05/fig/danieru.png")  #通常時の姿
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.invincible_image = pg.image.load("ex05/fig/supadanieru.png")  #無敵時の姿
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
            
    def player(self):
        return self.rect.topleft()

            
def check_collision(player, enemy):
    """
    衝突判定(通常時、無敵時の判定)
    """
    if not player.invincible:
        if player.rect.colliderect(enemy.rect):
            return True
    return False



class Enemy:
    """
    あくまで確認用のための敵
    チームメイトの方を優先する
    """
    def __init__(self):
        self.image = pg.image.load("ex05/fig/mukimuki.png") #確認用のため本来の敵画像とは違う
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.topright = (800, 400)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        

def main():
    # ゲームウィンドウの設定
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    
    # 画像の読み込みと初期化
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.rotozoom(kk_img,0,0.5)
    bg_imgs = [bg_img,pg.transform.flip(bg_img,True, False)]*2
    score = Score()
    coin = Coin(800, 600)

    
    # 主人公の初期設定
    player_y = 400 # 主人公のY座標の初期値
    player_y_vel = 0 # 主人公のY方向の速度の初期値
    jumping = False # ジャンプ中かどうかを表すフラグ 
    tmr = 0
    
    # 効果音の読み込み
    jump_sound = pg.mixer.Sound("ex05/fig/jump.mp3")
    
    player = Player()
    enemy = Enemy()
    
    font = pg.font.SysFont(None, 36)
    lshift_pressed = False
    
    
    tmr = 0
    
    
    score = 500  
    """
    確認のため初期値を５００にしている
    本来は０から開始する
    チームメイトの方を優先する
    """
    
    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                return
            if event.type == pg.QUIT: 
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not jumping:
                    player_y_vel = -20 # ジャンプ時のY方向の速度を設定
                    jumping = True # ジャンプ中のフラグを立てる
                    jump_sound.play() # ジャンプ効果音の再生
                elif event.key == pg.K_LSHIFT and not lshift_pressed:  #左シフトが押されているかの判定
                    lshift_pressed = True
                    if score >= 10:
                        player.set_invincible()
                        score -= 10
                """elif event.type == pg.KEYUP:
                    if event.key == pg.K_LSHIFT:
                        lshift_pressed = False
                    """
        player.update()
        enemy.update()
         
        if check_collision(player, enemy):  #衝突判定
            if not player.invincible:
                break
        
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])
        
        # ジャンプの処理
        if jumping:
            player_y_vel += 1 # 重力の影響を受けるため、Y方向の速度に重力を加える
            Player.player_y += player_y_vel # Y座標を速度に応じて更新
            if Player.player_y >= 400:
                Player.player_y = 400
                player_y_vel = 0
                jumping = False
                
        # 背景画像のスクロールと描画
        for i in range(4):
            screen.blit(bg_imgs[i], [1600*i-x, 0])
        if tmr % 100 <= 50:
            screen.blit(kk_img, [200, 400])
        else:            
            screen.blit(kk_img,[200,400])

        coin.update(screen)
        score.update(screen)

        if tmr % 550 == 0:    
            coin = Coin(screen.get_width(), screen.get_height())

        if coin.check_collision(kk_img.get_rect()):
            score.score_up(10) 
        if player.invincible:
            screen.blit(player.image, [200,Player.player_y])
        else:
            if tmr % 100 <= 50:
                screen.blit(player.image, [200,Player.player_y])
            else:
                screen.blit(player.image, [200,Player.player_y])
                
        # 主人公の描画    
        pg.display.update()
        tmr += 1        
        clock.tick(100)
        
        screen.blit(enemy.image, enemy.rect.topleft)
        
        
        """
        スコアの表示
        あくまでこれも確認用のチームメイトの方を優先する
        """
        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        screen.blit(score_text, (650, 20))



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    