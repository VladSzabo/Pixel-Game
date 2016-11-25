"""
    Copyright (c) 2016: Szabo Vlad
    Game Engine for Pygame, including:
        - Entities
        - Collisions
        - Main class, with game loop
"""
from __future__ import print_function
import pygame
from math import cos, sin, radians
from threading import Thread
import socket
import asyncore


class App(object):
    clock = pygame.time.Clock()
    game_exit = False

    def __init__(self, title, width, height, background_color):
        self.title = title
        self.width = width
        self.height = height
        self.background_color = background_color

        pygame.init()
        self.game_display = pygame.display.set_mode((width, height), pygame.SRCALPHA)
        pygame.display.set_caption(title)
        self.main_loop()

    def main_loop(self):
        while not self.game_exit:

            for event in pygame.event.get():
                self.handle_keys(event)

            self.game_display.fill(self.background_color)
            self.render(self.game_display)
            pygame.display.update()
            self.update()
            self.clock.tick(60)

    def render(self, game_display):
        pass

    def update(self):
        pass

    def handle_keys(self, event):
        if event.type == pygame.QUIT:
            self.game_exit = True


class Entity(object):
    def __init__(self, image, draw_box, collision, id_entity):
        self.image = image
        self.image = pygame.transform.scale(self.image, (draw_box[2], draw_box[3]))

        self.draw_box = draw_box
        self.collision = collision
        self.id_entity = id_entity

    def update(self):
        pass

    def render(self, game_display):
        game_display.blit(self.image, self.draw_box)

    def move(self, dir_x, dir_y, speed, collision_list):
        if not self.collision_detection(collision_list, dir_x, dir_y, speed):
            self.draw_box[0] += cos(radians(dir_x)) * speed
            self.draw_box[1] += sin(radians(dir_y)) * speed

    def collision_detection(self, collision_list, dir_x, dir_y, speed):
        col = False

        for c in collision_list:
            if self.id_entity != c.id_entity:
                if 'list' in str(type(self.collision[0])):
                    for my_rect in self.collision:

                        new_rect = [my_rect[0] + cos(radians(dir_x)) * speed, my_rect[1] + sin(radians(dir_y)) * speed,
                                    my_rect[2], my_rect[3]]

                        if 'list' in str(type(c.collision[0])):
                            for c_rect in c.collision:
                                if pygame.Rect(new_rect).colliderect(pygame.Rect(c_rect)):
                                    col = True
                                    break
                            if col:
                                break
                        else:
                            if pygame.Rect(new_rect).colliderect(pygame.Rect(c.collision)):
                                col = True
                                break
                    if col:
                        break
                else:

                    new_rect = [self.collision[0] + cos(radians(dir_x)) * speed,
                                self.collision[1] + sin(radians(dir_y)) * speed,
                                self.collision[2], self.collision[3]]

                    if 'list' in str(type(c.collision[0])):
                        for c_rect in c.collision:
                            if pygame.Rect(new_rect).colliderect(pygame.Rect(c_rect)):
                                col = True
                                break
                        if col:
                            break
                    else:
                        if pygame.Rect(new_rect).colliderect(pygame.Rect(c.collision)):
                            col = True
                            break
        return col


class Client(object):

    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    playersConnected = 1
    firstTimeConnect = True
    my_id = None

    def __init__(self, ip):
        if ip is None:
            ip = socket.gethostname()
            self.tcpCliSock.connect((ip, 21567))
        else:
            self.tcpCliSock.connect((ip, 21567))
        print("Client connected to IP: " + str(ip))
        Client.start_client()

    @staticmethod
    def send(message):
        Client.tcpCliSock.send(message)

    @staticmethod
    def socket():
        def loop0():
            while 1:
                data = Client.tcpCliSock.recv(1024)
                if data:
                    print("Client Received: " + str(data))
                    Client.read_data(data)

        thread = Thread(target=loop0)
        thread.start()

    @staticmethod
    def start_client():
        Client.socket()
        Client.send("connect")

    @staticmethod
    def read_data(data):
        data = str(data)
        if "connect" in data:

            if Client.firstTimeConnect:
                Client.firstTimeConnect = False
                id_ = data.split("|")[1]
                Client.playersConnected = int(id_) + 1

                Client.my_id = int(id_)
            else:
                Client.playersConnected += 1


class Server(object):

    clients = {}
    clientsId = {}
    playersConnected = -1

    class MainServerSocket(asyncore.dispatcher):

        def __init__(self, port):
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.bind((socket.gethostname(), port))
            self.listen(5)

        def handle_accept(self):
            new_socket, address = self.accept()
            Server.clients[address] = new_socket
            Server.playersConnected += 1
            Server.clientsId[address] = Server.playersConnected

            print("Connected from", address)
            Server.SecondaryServerSocket(new_socket)

    class SecondaryServerSocket(asyncore.dispatcher_with_send):

        def handle_read(self):
            received_data = self.recv(8192)
            if received_data:

                received_data = str(received_data)
                print("Server received: " + received_data)

                player = None
                if "|" in str(received_data):
                    player = str(received_data).split("|")
                    player = player[1]

                if "connect" in received_data:
                    received_data = received_data + "|" + str(Server.playersConnected)

                for key in Server.clients:
                    if player is None:
                        Server.clients[key].send(received_data)
                    elif Server.clientsId[key] != int(player):
                        Server.clients[key].send(received_data)
            else:
                self.close()

        def handle_close(self):
            print("Disconnected from", self.getpeername())
            one = self.getpeername()
            Server.playersConnected -= 1
            del Server.clients[one]
            del Server.clientsId[one]

    def __init__(self):
        thread = Thread(target=Server.start_server)
        thread.start()

    @staticmethod
    def start_server():
        Server.MainServerSocket(80)
        asyncore.loop()
