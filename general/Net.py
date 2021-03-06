from general.Constants import Constants
import socket
from threading import Thread
from world.World import Map
from gui.Messages import Messages

class Client(object):

    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    playersConnected = 1
    firstTimeConnect = True
    my_id = None

    def __init__(self, ip, port):
        if ip is None:
            ip = socket.gethostname()
            self.tcpCliSock.connect((ip, port))
        else:
            self.tcpCliSock.connect((ip, port))
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

                print("Your id is: ", Client.my_id)

                Constants.add_player(Client.my_id)

                if Client.my_id > 0:
                    for i in range(Client.my_id):
                        Constants.add_player(i)

            else:
                if not int(data.split("|")[1]) < Client.playersConnected:
                    Constants.add_player(Client.playersConnected)
                    Client.playersConnected += 1

        else:
            data_chunks = data.split("?")
            for packet in data_chunks:
                if "coord" in packet:
                    info = packet.split("|")
                    player = Constants.get_player_by_id(int(info[1]))
                    player.set_pos(int(info[2]), int(info[3]))

                elif "shift" in packet:
                    info = packet.split("|")
                    player = Constants.get_player_by_id(int(info[1]))
                    Map.world[int(info[3])][int(info[2])].image_fore = player.color + (100,)
                    Map.world[int(info[3])][int(info[2])].collide = True

                elif "ctrl" in packet:
                    info = packet.split("|")
                    Map.world[int(info[3])][int(info[2])].image_fore = None
                    Map.world[int(info[3])][int(info[2])].collide = False

                elif "bullet" in packet:
                    info = packet.split("|")
                    player = Constants.get_player_by_id(int(info[1]))
                    player.add_bullet(int(info[2]), int(info[3]), int(info[4]))

                elif "msg" in packet:
                    info = packet.split("|")
                    Messages.add_message(info[2])

                elif "dmg" in packet:
                    info = packet.split("|")
                    mobs = Constants.get_all_mobs()
                    for mob in mobs:
                        if mob.id == int(info[2]):
                            mob.health -= int(info[3])
                            break

                elif "spawn" in packet:
                    info = packet.split("|")
                    Constants.add_mob(info[2], int(info[3]), int(info[4]), int(info[5]))

                elif "mob" in packet:
                    info = packet.split("|")
                    mobs = Constants.get_all_mobs()
                    for mob in mobs:
                        if mob.id == int(info[2]):
                            mob.x = int(info[3])
                            mob.y = int(info[4])