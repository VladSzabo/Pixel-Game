import pygame


class Constants(object):
    sX = 0
    sY = 0
    width = 0
    height = 0
    block_size = 1. / 40

    map_width_screen = 0
    map_height_screen = 0

    A, W, S, D = False, False, False, False
    SHIFT, CTRL = False, False
    HOST = False

    images = {
        "block": pygame.image.load("res/block.png"),
        "zombie": pygame.image.load("res/zombie.png"),
        "skeleton": pygame.image.load("res/skeleton.png")
    }
    fonts = {
        "font1": None
    }

    def __init__(self):
        Constants.map_width_screen = int(Constants.block_size ** -1)
        Constants.block_size *= Constants.width
        Constants.map_height_screen = int(Constants.map_width_screen * Constants.height / Constants.width)
        for i in Constants.images.keys():
            Constants.images[i] = pygame.transform.scale(Constants.images[i], (int(Constants.block_size),
                                                         int(Constants.block_size)))

        Constants.fonts["font1"] = pygame.font.Font("Res/font1.ttf", int(Constants.block_size / 1.5))
        Constants.fonts["font1"].set_bold(True)

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
    def get_all_mobs():
        from entities.Entities import Entities
        mobs = Entities.mobs
        del Entities
        return mobs

    @staticmethod
    def get_players_pos():
        from entities.Entities import Entities
        players = Entities.players
        del Entities
        return [(i.x, i.y) for i in players]

    @staticmethod
    def get_main_player_coord():
        from entities.Entities import Entities
        player = Entities.players[0]
        del Entities
        return player.x, player.y

    @staticmethod
    def add_player(id_):
        from entities.Entities import Entities
        Entities.add_player(id_)

    @staticmethod
    def add_mob(t, id_, x, y):
        from entities.Entities import Entities
        Entities.add_mob(t, id_, x, y)