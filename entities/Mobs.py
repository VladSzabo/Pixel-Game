from entities.Entity import Entity
from general.Constants import Constants
from random import randint


class Zombie(Entity):

    def __init__(self, x, y):
        image = Constants.images["zombie"]
        template = [[[0, 0], image], [[0, 1], image]]

        super(self.__class__, self).__init__(x, y, template, 1./5)
        del image, template

    def update(self):
        super(self.__class__, self).update()

        player_pos = self.get_closest_player_pos()

        if player_pos[0] > self.x:
            dir_x = 1
        elif player_pos[0] < self.x:
            dir_x = -1
        else:
            dir_x = 0

        if player_pos[1] > self.y:
            dir_y = 1
        elif player_pos[1] < self.y:
            dir_y = -1
        else:
            dir_y = 0

        self.move(dir_x, dir_y)
        print(self.path_obstructed(dir_x, dir_y, player_pos[0], player_pos[1]))


