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
JUMP = -25
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
        super().__init__(W // 2, FLOOR_Y, "assets/Player_grey.jpg")

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


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, is_hazard=False):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.color = (255, 50, 50) if is_hazard else (120, 120, 120)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hazard = is_hazard

def game():
    clock = pg.time.Clock()

    player = Player()
    
    player.rect.midbottom = (W // 2, FLOOR_Y)
    player.speed = 0
    player.on_ground = True

    all_sprites = pg.sprite.Group()
    all_sprites.add(player)

    platforms = pg.sprite.Group()
    hazards = pg.sprite.Group()
    
    level_data = [
        (0, H - 30, W, 30, True),                     
        (W // 2 - 150, FLOOR_Y, 300, 20, False),      
        (700, 800, 250, 30, False),                 
        (400, 650, 300, 30, False),                  
        (50, 520, 300, 30, False),                   
        (350, 380, 300, 30, False),                  
        (700, 240, 250, 30, False),                   
        (200, 120, 400, 30, False)                   
    ]
    
    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        if p[4]:  
            hazards.add(plat)
        else:
            platforms.add(plat)

    running = True
    while running:
        old_x = player.rect.x
        old_y = player.rect.y

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player.on_ground:
                    player.speed = JUMP
                    player.on_ground = False

        all_sprites.update()

        if pg.sprite.spritecollideany(player, hazards):
            player.kill()

        hits = pg.sprite.spritecollide(player, platforms, False)
        if hits:
            for hit in hits:
                if player.speed > 0 and old_y + player.rect.height <= hit.rect.top + player.speed + 1:
                    player.rect.bottom = hit.rect.top
                    player.speed = 0
                    player.on_ground = True
                elif player.speed < 0 and old_y >= hit.rect.bottom + player.speed - 1:
                    player.rect.top = hit.rect.bottom
                    player.speed = 0
                else:
                    if old_x + player.rect.width <= hit.rect.left + 5:
                        player.rect.right = hit.rect.left
                    elif old_x >= hit.rect.right - 5:
                        player.rect.left = hit.rect.right

        if player.dead:
            running = False

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    game()
