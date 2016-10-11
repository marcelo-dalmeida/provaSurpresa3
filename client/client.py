__author__ = 'Marcelo d\'Almeida'

import random
import socket

class Client:


    def __init__(self, square_matrix_size):
        self._socket = socket.socket()
        self._host = socket.gethostname()
        self._port = 5000

        self._client_name = "client_" + str(random.randint(10000000, 100000000))

        self._matrix_1_filename = None
        self._matrix_2_filename = None
        self._square_matrix_size = square_matrix_size

        self.create_data()

        self.send_client_data()

    def create_data(self):

        self._matrix_1_filename = "matrix_1_" + self._client_name + ".txt"
        self._matrix_2_filename = "matrix_2_" + self._client_name + ".txt"

        matrix_1_file = open(self._matrix_1_filename, "wb")
        matrix_2_file = open(self._matrix_2_filename, "wb")

        print("Matrix 1")
        self.create_matrix(matrix_1_file)

        print("Matrix 2")
        self.create_matrix(matrix_2_file)

    def send_client_data(self):
        self.send_client_name()
        self.send_matrix(self._matrix_1_filename)
        self.send_matrix(self._matrix_2_filename)
        self.recv_final_ack()

    def create_matrix(self, matrix_file):
        for i in range(0, self._square_matrix_size):
            for j in range(0, self._square_matrix_size):
                number = random.randint(0, 100)
                print(number, end=" ")
                matrix_file.write((str(number) + " ").encode())
            print()
            if i != self._square_matrix_size - 1:
                matrix_file.write("\n".encode())
        print()
        matrix_file.close()

    def send_client_name(self):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        self._socket.send(self._client_name.encode())
        self._socket.close()

    def send_matrix(self, matrix_filename):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        matrix_file = open(matrix_filename, "rb")
        matrix = matrix_file.read(1024)
        self._socket.send(matrix)
        self._socket.close()

    def recv_final_ack(self):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        print(self._socket.recv(1024).decode())
        self._socket.close()

client_node = Client(5)
