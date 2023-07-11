import sys
import pygame as pg


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
    
    # 主人公の初期設定
    player_y = 400 # 主人公のY座標の初期値
    player_y_vel = 0 # 主人公のY方向の速度の初期値
    jumping = False # ジャンプ中かどうかを表すフラグ 
    tmr = 0
    
    # 効果音の読み込み
    jump_sound = pg.mixer.Sound("ex05/fig/jump.mp3")
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not jumping:
                    player_y_vel = -20 # ジャンプ時のY方向の速度を設定
                    jumping = True # ジャンプ中のフラグを立てる
                    jump_sound.play() # ジャンプ効果音の再生
        x = tmr % 3200
        screen.blit(bg_img, [x, 0])
        
        # ジャンプの処理
        if jumping:
            player_y_vel += 1 # 重力の影響を受けるため、Y方向の速度に重力を加える
            player_y += player_y_vel # Y座標を速度に応じて更新
            if player_y >= 400:
                player_y = 400
                player_y_vel = 0
                jumping = False
                
        # 背景画像のスクロールと描画
        for i in range(4):
            screen.blit(bg_imgs[i], [1600*i-x, 0])
            
        # 主人公の描画    
        screen.blit(kk_img,[200,player_y])
        pg.display.update()
        tmr += 1        
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()