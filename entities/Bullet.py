import pygame
from general.Constants import Constants


class Bullet(object):

    alive = False

    def __init__(self, image, size, against_mobs):
        self.image = image
        self.size = size
        self.against_mobs = against_mobs
        self.pellets = []

    def start(self, point, dir_x, dir_y):
        pass

    def render(self, game_display):
        if "tuple" in str(type(self.image)):
            for p in self.pellets:
                rect = pygame.Surface((p[0][2], p[0][3]), pygame.SRCALPHA, 32)
                rect.fill(self.image)
                game_display.blit(rect, (p[0][0] - Constants.sX, p[0][1] - Constants.sY))
                del rect

    def update(self):
        if self.against_mobs:
            self.collide_with_mobs()
        else:
            self.collide_with_players()

        for p in self.pellets:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]

    def collide_with_mobs(self):
        pass

    def collide_with_players(self):
        pass
