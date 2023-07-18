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

def main():
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex05/fig/danieru.png")
    kk_img = pg.transform.rotozoom(kk_img,0,0.5)
    bg_imgs = [bg_img,pg.transform.flip(bg_img,True, False)]*2
    score = Score()
    coin = Coin(800, 600)

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])

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

        pg.display.update()
        tmr += 1        
        clock.tick(100)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()