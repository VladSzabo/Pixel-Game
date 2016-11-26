import pygame
from general.Constants import Constants
from math import cos, sin, radians
from general.Net import Client


class Bullet(object):
    alive = False
    life_counter = 0

    def __init__(self, image, size, against_mobs, life, speed, damage):
        self.image = image
        self.size = size
        self.against_mobs = against_mobs
        self.life = life
        self.speed = speed
        self.damage = damage
        self.pellets = []

    def start(self, point, angle):
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
            p[0][0] += cos(radians(p[1])) * self.speed
            p[0][1] += sin(radians(p[1])) * self.speed

        self.life_counter += 1

    def collide_with_mobs(self):
        mobs = Constants.get_all_mobs()
        for p in self.pellets:
            for mob in mobs:
                for info in mob.array:
                    if pygame.Rect(p[0][0], p[0][1], p[0][2], p[0][3]).colliderect(pygame.Rect(
                                    (mob.x + info[0][0]) * Constants.block_size,
                                    (mob.y + info[0][1]) * Constants.block_size,
                            Constants.block_size, Constants.block_size
                    )):
                        mob.health -= self.damage
                        self.life_counter = self.life
                        Client.send("dmg|" + str(Client.my_id) + "|" + str(mob.id) + "|" + str(self.damage) + "|?")

    def collide_with_players(self):
        pass
