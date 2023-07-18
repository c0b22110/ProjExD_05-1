import sys
import pygame as pg
"""
score,enemy
"""

class Player:  #プレイヤークラス
    def __init__(self):
        self.image = pg.image.load("ex05/fig/danieru.png")  #通常時の姿
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.invincible_image = pg.image.load("ex05/fig/supadanieru.png")  #無敵時の姿
        self.invincible_image = pg.transform.flip(self.invincible_image, True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 400)
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
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.flip(kk_img,True,False)
    kk_imgs = pg.transform.rotozoom(kk_img,0,0.5)
    bg_imgs = [bg_img,pg.transform.flip(bg_img,True, False)]*2
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
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT and not lshift_pressed:  #左シフトが押されているかの判定
                    lshift_pressed = True
                    if score >= 10:
                        player.set_invincible()
                        score -= 10
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    lshift_pressed = False
                    
        player.update()
        enemy.update()
        
        if check_collision(player, enemy):  #衝突判定
            if not player.invincible:
                break
        
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])

        for i in range(4):
            screen.blit(bg_imgs[i], [1600*i-x, 0])

        if player.invincible:
            screen.blit(player.image, player.rect.topleft)
        else:
            if tmr % 100 <= 50:
                screen.blit(player.image, player.rect.topleft)
            else:
                screen.blit(player.image, player.rect.topleft)
        
        screen.blit(enemy.image, enemy.rect.topleft)
        
        
        """
        スコアの表示
        あくまでこれも確認用のためチームメイトの方を優先する
        """
        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        screen.blit(score_text, (650, 20))
        
        
        pg.display.update()
        tmr += 1        
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
    