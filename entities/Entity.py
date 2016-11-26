from general.Constants import Constants
from world.World import Map
from math import sqrt


class Entity(object):
    tick = 0

    def __init__(self, id_, x, y, array, speed=1, health=100, damage=10, bullet=None):
        # [[[0, 0], "image"]]
        self.id = id_
        self.x = x
        self.y = y
        self.array = array
        self.health = health
        self.damage = damage
        self.bullet = bullet
        self.speed = int(speed ** (-1))

    def render(self, game_display):
        for info in self.array:
            game_display.blit(info[1], [(self.x + info[0][0]) * Constants.block_size - Constants.sX,
                                        (self.y + info[0][1]) * Constants.block_size - Constants.sY,
                                        Constants.block_size,
                                        Constants.block_size])

    def update(self):
        self.tick += 1
        if self.tick > 200:
            self.tick = 0

    def move(self, dir_x, dir_y):
        if self.tick % self.speed == 0:
            if not self.collision(dir_x, dir_y):
                self.x += dir_x
                self.y += dir_y
                return [True, True]
        else:
            return [True, False]
        return [False, False]

    def force_move(self, dir_x, dir_y):
        if self.tick % self.speed == 0:
            self.x += dir_x
            self.y += dir_y
            return True
        else:
            return False

    def collision(self, dir_x, dir_y):
        col = False
        for i in self.array:
            if 0 <= self.x + i[0][0] + dir_x < Map.width and 0 <= self.y + i[0][1] + dir_y < Map.height:
                if Map.world[self.y + i[0][1] + dir_y][self.x + i[0][0] + dir_x].collide:
                    col = True
            else:
                col = True

        return col

    def collision_with_mobs(self, dir_x, dir_y):
        mobs = Constants.get_all_mobs()

        for mob in mobs:
            if mob.id != self.id:
                for i in self.array:
                    for j in mob.array:
                        if self.x + dir_x + i[0][0] == mob.x + j[0][0] and self.y + dir_y + i[0][1] == mob.y + j[0][1]:
                            return True
        return False

    def get_closest_player_pos(self):

        players_pos = Constants.get_players_pos()
        min_distance = 99999
        x, y = 0, 0

        for pos in players_pos:
            distance = sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                x, y = pos[0], pos[1]

        return x, y

    def path_obstructed(self, dir_x, dir_y, target_x, target_y):
        obs = False
        tmp_x, tmp_y = self.x, self.y
        distance_now, distance_last = 999, 1000

        while distance_now < distance_last and not obs:

            distance_last = sqrt((tmp_x - target_x) ** 2 + (tmp_y - target_y) ** 2)
            for i in self.array:
                if 0 <= tmp_x + i[0][0] + dir_x < Map.width and 0 <= tmp_y + i[0][1] + dir_y < Map.height:
                    if Map.world[tmp_y + i[0][1] + dir_y][tmp_x + i[0][0] + dir_x].collide:
                        obs = True
                        break
                else:
                    obs = True
                    break
            tmp_x += dir_x
            tmp_y += dir_y
            distance_now = sqrt((tmp_x - target_x) ** 2 + (tmp_y - target_y) ** 2)

        return obs
