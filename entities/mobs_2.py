from entities.Entity import Entity
from general.Constants import Constants
from random import randint


class Skeleton(Entity):

    def __init__(self, x, y):
        image = Constants.images["skeleton"]
        template = [[[0, 0], image]]  # You will have to complete it
        health = 50
        speed = 1. / 4
        super(self.__class__, self).__init__(x, y, template, speed, health)

        del image, template

    def update(self):
        super(self.__class__, self).update()

        player_pos = self.get_closest_player_pos()

        if player_pos[0] - self.x in range(0, 10):
            dir_x = 1
        elif player_pos[0] - self.x in range(-9, 1):
            dir_x = -1
        else:
            dir_x = 0

        if player_pos[1] - self.y in range(0, 10):
            dir_y = 1
        elif player_pos[1] - self.y in range(-9, 1):
            dir_y = -1
        else:
            dir_y = 0

        self.move(dir_x, dir_y)
