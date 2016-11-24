import pygame


class Constants:

    sX = 0
    sY = 0
    width = 0
    height = 0
    block_size = 1 / 41

    map_width_screen = 40
    map_height_screen = 0

    A, W, S, D = False, False, False, False
    SHIFT = False

    images = {
        "block": pygame.image.load("res/block.png")
    }

    def __init__(self):
        Constants.block_size *= Constants.width
        Constants.map_height_screen = int(Constants.map_width_screen * Constants.height / Constants.width)

    @staticmethod
    def get_players():
        from entities.Entities import Entities
        return Entities.players

    @staticmethod
    def get_main_player_coord():
        from entities.Entities import Entities
        return Entities.players[0].x, Entities.players[0].y
