from entities.Player import Player
from general.Constants import Constants


class Entities:
    players = []

    def __init__(self):
        Entities.players.append(
            Player(0, (0, 0, 0), Constants.map_width_screen // 2, Constants.map_height_screen // 2))

    @staticmethod
    def render(game_display):
        for player in Entities.players:
            player.render(game_display)

    @staticmethod
    def update():
        for player in Entities.players:
            player.update()

