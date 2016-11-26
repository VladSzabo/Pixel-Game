from general.Constants import Constants
from world.World import Map
from general.Net import Client
from entities.Bullets import SimpleBullet
from pygame import mouse
from math import atan2, degrees, pi
from copy import deepcopy


class Player:
    health = 100
    tick = 0
    bullet_time, bullet_rate = 0, 5
    can_shoot = True
    frame_x, frame_y, max_frames = 1, 1, 3
    dir_x, dir_y = 1, 1

    def __init__(self, id_, color, x, y):
        self.id = id_
        self.color = color
        self.x = x
        self.y = y
        self.bullet = SimpleBullet(color + (180,))
        self.bullets = []

    def render(self, game_display):
        game_display.fill(self.color,
                          [self.x * Constants.block_size - Constants.sX, self.y * Constants.block_size - Constants.sY,
                           Constants.block_size, Constants.block_size])

        for bullet in self.bullets:
            if bullet.alive:
                bullet.render(game_display)

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

            if mouse.get_pressed()[0] == 1 and self.can_shoot:
                self.can_shoot = False

                mouse_pos = mouse.get_pos()
                my_pos = (self.x * Constants.block_size - Constants.sX, self.y * Constants.block_size - Constants.sY)
                angle = int(180 - Player.get_angle(mouse_pos[0], mouse_pos[1], my_pos[0], my_pos[1]))

                self.add_bullet(my_pos[0] + Constants.sX, my_pos[1] + Constants.sY, angle)

                Client.send("bullet|" + str(self.id) + "|" + str(int(my_pos[0] + Constants.sX)) + "|" +
                            str(int(my_pos[1] + Constants.sY)) + "|" + str(angle) + "|?")

            self.bullet_time += 1
            if self.bullet_time >= self.bullet_rate:
                self.can_shoot = True
                self.bullet_time = 0

            self.tick += 1
            if self.tick >= 600:
                self.tick = 0

        for bullet in self.bullets:

            if bullet.alive:
                bullet.update()
                if bullet.life_counter >= self.bullet.life:
                    bullet.life_counter = 0
                    bullet.alive = False

    def add_bullet(self, x, y, angle):
        self.bullet.start((x, y), angle)
        self.bullet.alive = True

        found_bullet = False

        for i in range(len(self.bullets)):
            if not self.bullets[i].alive:
                found_bullet = True
                self.bullets[i] = deepcopy(self.bullet)
                break

        if not found_bullet:
            self.bullets.append(deepcopy(self.bullet))

    def move(self, dir_x, dir_y):
        if self.tick % 6 == 0:
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

    def set_pos(self, x, y):
        self.x = x
        self.y = y

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

    @staticmethod
    def get_angle(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads)
