import pygame


class Constants(object):
    sX = 0
    sY = 0
    width = 0
    height = 0
    block_size = 1. / 41

    map_width_screen = 40
    map_height_screen = 0

    A, W, S, D = False, False, False, False
    SHIFT, CTRL = False, False

    images = {
        "block": pygame.image.load("res/block.png"),
        "zombie": pygame.image.load("res/zombie.png")
    }

    def __init__(self):
        Constants.block_size *= Constants.width
        Constants.map_height_screen = int(Constants.map_width_screen * Constants.height / Constants.width)
        for i in Constants.images.keys():
            Constants.images[i] = pygame.transform.scale(Constants.images[i], (int(Constants.block_size),
                                                         int(Constants.block_size)))

    @staticmethod
    def get_players():
        from entities.Entities import Entities
        return Entities.players

    @staticmethod
    def get_player_by_id(id_):
        from entities.Entities import Entities
        for player in Entities.players:
            if player.id == id_:
                return player

    @staticmethod
    def get_players_pos():
        from entities.Entities import Entities
        return [(i.x, i.y) for i in Entities.players]

    @staticmethod
    def get_main_player_coord():
        from entities.Entities import Entities
        return Entities.players[0].x, Entities.players[0].y

    @staticmethod
    def add_player(id_):
        from entities.Entities import Entities
        Entities.add_player(id_)