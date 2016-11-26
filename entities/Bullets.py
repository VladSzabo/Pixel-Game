from entities.Bullet import Bullet
from general.Constants import Constants


class SimpleBullet(Bullet):

    def __init__(self, color):
        super(self.__class__, self).__init__(int(Constants.block_size / 10.), color, True)

    def start(self, point, dir_x, dir_y):
        self.pellets = [[[point[0], point[1], self.size, self.size], dir_x, dir_y]]


