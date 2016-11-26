from entities.Player import Player
from general.Constants import Constants
from entities.Mobs import Zombie
from entities.mobs_2 import Skeleton
from general.Net import Client
from random import randint
from world.World import Map


class Entities:
    players = []
    mobs = []
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    wave = 1
    timer = 0

    def __init__(self):
        pass

    @staticmethod
    def render(game_display):
        c = 0
        while c < len(Entities.mobs):
            Entities.mobs[c].render(game_display)
            c += 1
        for player in Entities.players:
            player.render(game_display)

    @staticmethod
    def update():
        for player in Entities.players:
            player.update()

        c = 0
        while c < len(Entities.mobs):
            Entities.mobs[c].update()
            if Entities.mobs[c].health <= 0:
                Entities.mobs.pop(c)
                c -= 1
            c += 1

        if Constants.HOST:
            if len(Entities.mobs) == 0:

                Entities.generate_wave()
            Entities.timer += 1
            if Entities.timer > 1000:
                Entities.timer = 0

            if Entities.timer % 50 == 0:
                for i in range(len(Entities.mobs)):
                    Client.send("mob|0|" + str(i) + "|" + str(Entities.mobs[i].x) + "|" + str(Entities.mobs[i].y) + "|?")

    @staticmethod
    def generate_wave():
        Client.send(
            "msg|-1|Wave " + str(Entities.wave) + ": " + str(3 * Entities.wave) + " zombies will spawn|?")
        for i in range(3 * Entities.wave):
            Client.send("spawn|-1|z|" + str(i) + "|" + str(randint(0, Map.width - 1)) + "|" + str(randint(0, Map.height - 1)) + "|?")

        Entities.wave += 1

    @staticmethod
    def add_mob(t, id_, x, y):
        if "z" in t:
            Entities.mobs.append(Zombie(id_, x, y))

    @staticmethod
    def add_player(id_):
        Entities.players.append(Player(id_, Entities.colors[id_], Constants.map_width_screen / 2,
                                       Constants.map_height_screen / 2))
