__author__ = 'Marcelo d\'Almeida'

import socket
from server_side.management_thread import ManagementThread


class Server:
    new_clients_port_number = 5000
    port_number = 5001

    def __init__(self):
        self._shutdown = False

        self._socket = socket.socket()
        host = socket.gethostname()

        self._socket.bind((host, Server.new_clients_port_number))

        self._socket.listen()

        self.run()

    def run(self):

        while not self._shutdown:
            client, address = self._socket.accept()
            print('Got connection from', address)
            client.send(str(Server.port_number).encode())
            print(),

            thread = ManagementThread(Server.port_number)
            thread.start()

            Server.port_number += 1

            #self._shutdown = True

server_node = Server()
