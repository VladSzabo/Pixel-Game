import pygame
from GameEngine import App, Server
from general.Constants import Constants
from world.World import Map
from entities.Entities import Entities
from general.Net import Client


class Game(App):

    def __init__(self, title, width_, height_, background_color=(255, 255, 255)):
        Map()
        Entities()
        super(self.__class__, self).__init__(title, width_, height_, background_color)

    def render(self, game_display):
        Map.render(game_display)
        Entities.render(game_display)

    def update(self):
        Entities.update()

    def handle_keys(self, event):
        super(self.__class__, self).handle_keys(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Constants.A = True
            if event.key == pygame.K_w:
                Constants.W = True
            if event.key == pygame.K_s:
                Constants.S = True
            if event.key == pygame.K_d:
                Constants.D = True
            if event.key == pygame.K_LSHIFT:
                Constants.SHIFT = True
            if event.key == pygame.K_LCTRL:
                Constants.CTRL = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Constants.A = False
            if event.key == pygame.K_w:
                Constants.W = False
            if event.key == pygame.K_s:
                Constants.S = False
            if event.key == pygame.K_d:
                Constants.D = False
            if event.key == pygame.K_LSHIFT:
                Constants.SHIFT = False
            if event.key == pygame.K_LCTRL:
                Constants.CTRL = False

if __name__ == "__main__":
    info = open("settings.txt")
    connection_type = info.readline().replace("\n", "").replace(" ", "").split("=")[1]
    ip = info.readline().replace("\n", "").replace(" ", "").split("=")[1]
    port = int(info.readline().replace("\n", "").replace(" ", "").split("=")[1])
    Constants.width = int(info.readline().replace("\n", "").replace(" ", "").split("=")[1])
    Constants.height = int(info.readline().replace("\n", "").replace(" ", "").split("=")[1])
    info.close()

    Constants()

    if connection_type == "server":
        Server(port)
        Client(None, port)
    else:
        Client(ip, port)

    Game("Game", Constants.width, Constants.height)

    pygame.quit()
    quit()
