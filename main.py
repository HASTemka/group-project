import random
import random as rdm

import pygame as pg
import pygame_menu as pgm

pg.init()
pg.display.set_caption("Platformer")
W = 1024
H = 1024
screen = pg.display.set_mode((W, H))
GRAVITY = 1
JUMP = -30
PLAYER_SIZE = 80
FLOOR_Y = H - 50

class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.dead = False

    def update(self):
        super().update()

    def draw(self):
        screen.blit(self.image, self.rect)

    def kill(self):
        self.dead = True
        super().kill()

class Player(Sprite):
    def __init__(self):
        super().__init__(W // 2, FLOOR_Y, "IMG/Player_grey.jpg")

        self.image = pg.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))

        self.image_left = self.image
        self.image_right = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom=(W // 2, FLOOR_Y))

        self.speed = 0
        self.on_ground = True

    def update(self):
        if self.dead:
            return

        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.rect.x -= 5
            self.image = self.image_left

        if keys[pg.K_d]:
            self.rect.x += 5
            self.image = self.image_right

        if self.rect.left > W:
            self.rect.right = 0

        if self.rect.right < 0:
            self.rect.left = W

        self.speed += GRAVITY
        self.rect.y += self.speed

        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.speed = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self):
        screen.blit(self.image, self.rect)

def game():
    clock = pg.time.Clock()

    player = Player()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.on_ground:
                    player.speed = JUMP
                    player.on_ground = False

        all_sprites.update()

        if player.dead:
            running = False

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    game()