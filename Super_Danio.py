import sys
import pygame as pg
import time


class Power:

    def __init__(self, score):
        self.score = score
        self.power = False
        self.da_img = pg.image.load("ex05/fig/danieru.png")
        self.da_img = pg.transform.rotozoom(self.da_img, 0, 0.5)
        self.po_img = pg.image.load("ex05/fig/power.png")
        self.po_imgs = pg.transform.rotozoom(pg.transform.flip(self.po_img, True, False), 0, 0.5)  # デフォルトのimage
        self.now_img = self.da_img
    
    def update(self):
        if self.score >= 5 and not self.power:
            self.power_up()
        if self.score == 4:
            self.sound()

    def power_up(self):
        self.power = True
        self.now_img = self.po_imgs
    
    def draw(self, screen, x, y):
        screen.blit(self.now_img, (x, y))

    def sound(self):
        pg.mixer.init()
        pg.mixer.music.load("ex05/fig/power.mp3")
        pg.mixer.music.play()

def main():
    pg.display.set_caption("スーパーダニエル")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    # da_img = pg.image.load("ex05/fig/danieru.png")
    # da_img = pg.transform.rotozoom(da_img,0,0.5)
    bg_imgs = [bg_img,pg.transform.flip(bg_img,True, False)]*2

    tmr = 0
    score = 0  #実行用（後で削除）
    player_y = 400 #実行用（後で削除）
    width = 800 #実行用（後で削除）
    height = 600 #実行用（後で削除）
    screen = pg.display.set_mode((width, height)) #実行用（後で削除）
    pg.display.set_caption("Score Example") #実行用（後で削除）
    font = pg.font.Font(None, 36) #実行用（後で削除）
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            elif event.type == pg.KEYDOWN: #実行用（後で削除）
                if event.key == pg.K_SPACE: #実行用（後で削除）
                    score += 1 #実行用（後で削除）
        
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])
        for i in range(4):
            screen.blit(bg_imgs[i], [1600*i-x, 0])
        score_text = font.render("Score: {}".format(score), True, (0, 0, 0)) #実行用（後で削除）
        screen.blit(score_text, (10, 10))#実行用（後で削除）
        power = Power(score)
        power.update()
        power.draw(screen, 200, player_y)
        pg.display.update()
        tmr += 1        
        clock.tick(100)
 


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()