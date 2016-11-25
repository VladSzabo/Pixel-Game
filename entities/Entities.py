from entities.Player import Player
from general.Constants import Constants
from entities.Mobs import Zombie


class Entities:
    players = []
    mobs = []

    def __init__(self):
        Entities.players.append(
            Player(0, (0, 0, 0), Constants.map_width_screen // 2, Constants.map_height_screen // 2))
        Entities.mobs.append(
            Zombie(1, 1)
        )

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

