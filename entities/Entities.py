from entities.Player import Player
from general.Constants import Constants
from entities.Mobs import Zombie
from entities.mobs_2 import Skeleton


class Entities:
    players = []
    mobs = []
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    def __init__(self):
        """
        Entities.mobs += [
            Zombie(20, 20),
            Skeleton(1, 1)
         ]
         """

    @staticmethod
    def render(game_display):
        for mob in Entities.mobs:
            mob.render(game_display)
        for player in Entities.players:
            player.render(game_display)

    @staticmethod
    def update():
        for player in Entities.players:
            player.update()
        for mob in Entities.mobs:
            mob.update()

    @staticmethod
    def add_player(id_):
        Entities.players.append(Player(id_, Entities.colors[id_], Constants.map_width_screen / 2,
                                Constants.map_height_screen / 2))
