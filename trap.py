"""
код для ловушек картинку найдете если ненайдете то напишити  тогда я найду)
"""

import pygame


TRAP_COLOR = (100, 20, 20)
TRAP_HIGHLIGHT = (230, 80, 80)
class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y, size=40):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(TRAP_COLOR)
        pygame.draw.rect(self.image, TRAP_HIGHLIGHT, (0, 0, size, size), 3)
        self.rect = self.image.get_rect(topleft=(x, y))

