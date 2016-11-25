from entities.Entity import Entity
from general.Constants import Constants
from random import randint


class Skeleton(Entity):

    def __init__(self, x, y):
        image = Constants.images["zombie"]
        template = [[[0, 0], image], [[1, 1], image]]  # You will have to complete it
        health = 50
        speed = 1. / 4
        super(self.__class__, self).__init__(x, y, template, speed, health)

        del image, template

    def update(self):
        super(self.__class__, self).update()

        player_pos = self.get_closest_player_pos()


