from general.Constants import Constants
from world.World import Map
from general.Net import Client


class Player:

    health = 100
    tick = 0

    def __init__(self, id_, color, x, y):
        self.id = id_
        self.color = color
        self.x = x
        self.y = y

    def render(self, game_display):
        game_display.fill(self.color,
                          [self.x * Constants.block_size - Constants.sX, self.y * Constants.block_size - Constants.sY,
                           Constants.block_size, Constants.block_size])

    def update(self):
        if self.id == Client.my_id:
            if Constants.A:
                self.move(-1, 0)
            if Constants.W:
                self.move(0, -1)
            if Constants.D:
                self.move(1, 0)
            if Constants.S:
                self.move(0, 1)

            self.tick += 1
            if self.tick >= 600:
                self.tick = 0

    def move(self, dir_x, dir_y):
        if self.tick % 3 == 0:
            if not self.collision(dir_x, dir_y, Constants.CTRL):

                if Constants.SHIFT:
                    Map.world[self.y][self.x].image_fore = self.color + (100,)
                    Map.world[self.y][self.x].collide = True
                    Client.send("shift|" + str(self.id) + "|" + str(self.x) + "|" + str(self.y) + "|?")

                self.x += dir_x
                self.y += dir_y
                Client.send("coord|" + str(self.id) + "|" + str(self.x) + "|" + str(self.y) + "|?")

                Constants.sX += dir_x * Constants.block_size
                Constants.sY += dir_y * Constants.block_size

                if Constants.CTRL and Map.world[self.y][self.x].image_fore == self.color + (100,):
                    Map.world[self.y][self.x].image_fore = None
                    Map.world[self.y][self.x].collide = False
                    Client.send("ctrl|" + str(self.id) + "|" + str(self.x) + "|" + str(self.y) + "|?")

    def collision(self, dir_x, dir_y, ctrl):
        col = False
        if 0 <= self.x + dir_x < Map.width and 0 <= self.y + dir_y < Map.height:
            if Map.world[self.y + dir_y][self.x + dir_x].collide:
                if ctrl and Map.world[self.y + dir_y][self.x + dir_x].image_fore == self.color + (100,):
                    col = False
                else:
                    col = True
        else:
            col = True
        return col
