import tkinter
from PIL import Image, ImageTk, ImageOps
import random

# アプリの設定
VIEW_WIDTH = 600
VIEW_HEIGHT = 400
GAME_WIDTH = 1500

UPDATE_TIME = 100

BG_IMAGE_PATH = "ex05/fig/pg_bg.jpg"
PLAYER_IMAGE_PATH = "ex05/fig/danieru.png"

class Character:

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2

    JUMP_NO = 0
    JUMP_UP = 1
    JUMP_DOWN = 2

    def __init__(self):
        self.prepareImage(PLAYER_IMAGE_PATH, (100, 100))

        self.base_y = VIEW_HEIGHT - self.right_image.height()
        self.x = 0
        self.y = self.base_y
        self.speed_x = 30
        self.speed_y = 20
        self.jump_state = Character.JUMP_NO
        self.jump_height = 200
        self.direction = Character.DIRECTION_RIGHT

    def getImage(self):
        if self.direction == Character.DIRECTION_RIGHT:
            return self.right_image
        elif self.direction == Character.DIRECTION_LEFT:
            return self.left_image
    
    def prepareImage(self, path, size, is_right=True):
        image = Image.open(path)

        width, height = size
        ratio = min(width / image.width, height/ image.height)
        resize_size = (round(ratio * image.width), round(ratio * image.height))
        resized_image = image.resize(resize_size)
        mirrored_image = ImageOps.mirror(resized_image)

        if is_right:
            self.right_image = ImageTk.PhotoImage(resized_image)
            self.left_image = ImageTk.PhotoImage(mirrored_image)
        else:
            self.left_image = ImageTk.PhotoImage(resized_image)
            self.right_image = ImageTk.PhotoImage(mirrored_image)

    def move(self, direction):
        if direction == Character.DIRECTION_LEFT:
            self.x = max(0, self.x - self.speed_x)
            self.direction = Character.DIRECTION_LEFT
        elif direction == Character.DIRECTION_RIGHT:
            self.x = min(GAME_WIDTH - self.right_image.width(), self.x + self.speed_x)
            self.direction = Character.DIRECTION_RIGHT
        elif direction == Character.DIRECTION_UP:
            if self.jump_state == Character.JUMP_NO:
                self.jump_state = Character.JUMP_UP

    def update(self):
        if self.jump_state == Character.JUMP_UP:
            self.y -= self.speed_y
            if self.y <= self.base_y - self.jump_height:
                self.jump_state = Character.JUMP_DOWN
                self.y = self.base_y - self.jump_height
        elif self.jump_state == Character.JUMP_DOWN:
            self.y += self.speed_y
            if self.y >= self.base_y:
                self.jump_state = Character.JUMP_NO
                self.y = self.base_y

class Player(Character):

    def __init__(self):
        pass

class Enemy(Character):

    def __init__(self):
        pass

class CatEnemy(Enemy):

    def __init__(self):
        pass

class DogEnemy(Enemy):

    def __init__(self):
        pass

class Goal(Character):

    def __init__(self):
        pass

class Screen:

    def __init__(self, master):
        self.master = master

        self.view_width = VIEW_WIDTH
        self.view_height = VIEW_HEIGHT
        self.game_width = GAME_WIDTH
        self.game_height = self.view_height
        self.draw_images = []

        self.createWidgets()
        self.drawBackground()

    def createWidgets(self):
        self.canvas = tkinter.Canvas(
            self.master,
            width=self.view_width,
            height=self.view_height,
            scrollregion= (
                0,0,self.game_width,self.game_height
            ),
            highlightthickness=0
        )
        self.canvas.grid(column=0, row=0)

        xbar = tkinter.Scrollbar(
            self.master,
            orient=tkinter.HORIZONTAL,
        )

        xbar.grid(
            row=1, column=0,
            sticky=tkinter.W + tkinter.E
        )

        xbar.config(
            command=self.canvas.xview
        )

        self.canvas.config(
            xscrollcommand=xbar.set
        )

    def drawBackground(self):
        image = Image.open(BG_IMAGE_PATH)

        size = (self.game_width, self.game_height)
        resized_image = image.resize(size)

        self.bg_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(
            0, 0,
            anchor=tkinter.NW,
            image=self.bg_image
        )

    def update(self, image_infos):
        for draw_image in self.draw_images:
            self.canvas.delete(draw_image)

        self.draw_images.clear()
        
        for image, x, y in image_infos:

            draw_image = self.canvas.create_image(
                x, y,
                anchor=tkinter.NW,
                image=image
            )
            self.draw_images.append(draw_image)
    

class Game:

    def __init__(self, master):
        self.master = master
        self.screen = Screen(self.master)

        self.characters = []
        self.player = Character()
        self.characters.append(self.player)

        self.master.bind("<KeyPress-Left>", self.press)
        self.master.bind("<KeyPress-Right>", self.press)
        self.master.bind("<KeyPress-Up>", self.press)

        self.update()

    def press(self, event):
        if event.keysym == "Left":
            self.player.move(Character.DIRECTION_LEFT)
            
        elif event.keysym == "Right":
            self.player.move(Character.DIRECTION_RIGHT)

        elif event.keysym == "Up":
            self.player.move(Character.DIRECTION_UP)

    def update(self):
        self.master.after(UPDATE_TIME, self.update)

        for character in self.characters:
            character.update()

        image_infos = []
        for character in self.characters:

            image = character.getImage()

            image_info = (image, character.x, character.y)
            image_infos.append(image_info)

        self.screen.update(image_infos)


def main():
    app = tkinter.Tk()
    game = Game(app)
    app.mainloop()

if __name__ == "__main__":
    main()