import pygame
from general.Constants import Constants


class Block:
    def __init__(self, image_bg, image_fore, rect, collide):
        self.image_bg = image_bg
        self.image_fore = image_fore

        self.rect = rect
        self.collide = collide

    timer = 0

    def render(self, game_display):
        if self.image_bg is not None and "tuple" not in str(type(self.image_bg)):
            game_display.blit(self.image_bg,
                              [self.rect[0] - Constants.sX, self.rect[1] - Constants.sY, self.rect[2], self.rect[3]])

        elif "tuple" in str(type(self.image_bg)):
            game_display.fill(self.image_bg,
                              [self.rect[0] - Constants.sX, self.rect[1] - Constants.sY, self.rect[2], self.rect[3]])

        if self.image_fore is not None and "tuple" not in str(type(self.image_fore)):
            game_display.blit(self.image_fore,
                              [self.rect[0] - Constants.sX, self.rect[1] - Constants.sY, self.rect[2], self.rect[3]])
        elif "tuple" in str(type(self.image_fore)):
            rect = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA, 32)
            rect.fill(self.image_fore)
            game_display.blit(rect, (self.rect[0] - Constants.sX, self.rect[1] - Constants.sY))
            del rect

    def update(self):
        if "tuple" in str(type(self.image_fore)):
            if self.image_fore[3] == 100:
                self.timer += 1
                if self.timer >= 600:
                    self.image_fore = None
                    self.collide = False
                    self.timer = 0


class Map:
    world = []
    width, height = None, None

    def __init__(self, width=100, height=100):

        Map.width = width
        Map.height = height

        block_image = Constants.images["block"]

        for i in range(height):
            Map.world.append([])
            for j in range(width):
                Map.world[len(Map.world) - 1].append(Block(block_image, None,
                                                           [int(j * Constants.block_size),
                                                            int(i * Constants.block_size), int(Constants.block_size),
                                                            int(Constants.block_size)], False))

    @staticmethod
    def render(game_display):

        player_coord = Constants.get_main_player_coord()

        for i in range(player_coord[1] - Constants.map_height_screen / 2,
                       player_coord[1] + Constants.map_height_screen / 2 + 1):
            for j in range(player_coord[0] - Constants.map_width_screen / 2,
                           player_coord[0] + Constants.map_width_screen / 2 + 1):

                if 0 <= i < Map.height and 0 <= j < Map.width:
                    Map.world[i][j].render(game_display)

    @staticmethod
    def update():
        for i in range(Map.height):
            for j in range(Map.width):
                Map.world[i][j].update()