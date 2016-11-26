from entities.Bullet import Bullet
from general.Constants import Constants


class SimpleBullet(Bullet):
    def __init__(self, color):
        super(self.__class__, self).__init__(color, int(Constants.block_size / 1.7), True, 200,
                                             Constants.block_size / 5, 25)

    def start(self, point, angle):
        self.pellets = [[[point[0], point[1], self.size, self.size], angle]]
