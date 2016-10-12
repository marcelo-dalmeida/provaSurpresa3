import random
import socket
import argparse

import client_side.util as util

class Client:


    def __init__(self, square_matrix_size):
        self._socket = socket.socket()
        self._host = socket.gethostname()
        self._port = 5000

        self._client_name = "client_" + str(random.randint(10000000, 100000000))

        self._matrix_1_filename = None
        self._matrix_2_filename = None
        self._square_matrix_size = square_matrix_size

        print(self._client_name)

        self.create_data()

        self.send_client_data()

    def create_data(self):

        self._matrix_1_filename = "matrix_1_" + self._client_name + ".txt"
        self._matrix_2_filename = "matrix_2_" + self._client_name + ".txt"

        matrix_1_file = open(util.INPUT_FOLDER + self._matrix_1_filename, "wb")
        matrix_2_file = open(util.INPUT_FOLDER + self._matrix_2_filename, "wb")

        print("Matrix 1")
        self.create_matrix(matrix_1_file)

        print("Matrix 2")
        self.create_matrix(matrix_2_file)

    def send_client_data(self):

        self._port = self.recv_comm_port()
        self.send_client_name()
        self.send_matrix(self._matrix_1_filename)
        self.send_matrix(self._matrix_2_filename)

        print("Multiplication matrix")
        self.recv_matrix()
        print()
        self.recv_time()
        print()

        print("Addition matrix")
        self.recv_matrix()
        print()
        self.recv_time()
        print()

        self.recv_final_ack()

    def create_matrix(self, matrix_file):
        for i in range(0, self._square_matrix_size):
            for j in range(0, self._square_matrix_size):
                number = random.randint(0, 100)
                print(number, end="\t")
                matrix_file.write((str(number) + "\t").encode())
            print()
            if i != self._square_matrix_size - 1:
                matrix_file.write("\n".encode())
        print()
        matrix_file.close()

    def recv_comm_port(self):
        return int(self.recv_data())

    def send_client_name(self):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        self._socket.send(self._client_name.encode())
        self._socket.close()

    def send_matrix(self, matrix_filename):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        matrix_file = open(util.INPUT_FOLDER + matrix_filename, "rb")

        matrix = matrix_file.read(1024)

        while matrix:
            self._socket.send(matrix)
            matrix = matrix_file.read(1024)
        self._socket.close()

    def recv_matrix(self):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))

        data = ''
        matrix = self._socket.recv(1024).decode()
        while (matrix):
            data += matrix
            matrix = self._socket.recv(1024).decode()
        print(data)

        self._socket.close()

    def recv_time(self):
        print(self.recv_data())
        print(self.recv_data())
        print(self.recv_data())

    def recv_final_ack(self):
        print(self.recv_data())

    def recv_data(self):
        self._socket = socket.socket()
        self._socket.connect((self._host, self._port))
        data = self._socket.recv(1024).decode()
        self._socket.close()
        return data




#
# Command line support
#
parser = argparse.ArgumentParser()
parser.add_argument("-ms", "--matrix_size")

args = parser.parse_args()

#
# Console support
#
if not args.matrix_size:
    matrix_size = int(input('Matrix_size input: ').lower())
else:
    matrix_size = int(args.matrix_size)

client_node = Client(matrix_size)
