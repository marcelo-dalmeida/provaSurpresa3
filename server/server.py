__author__ = 'Marcelo d\'Almeida'

import threading
import time
import socket

MATRIX_ADDER_THREAD = "Matrix Adder Thread"
MATRIX_MULTIPLIER_THREAD = "Matrix Multiplier Thread"

class Server:

    def __init__(self):
        self._socket = socket.socket()
        self._host = socket.gethostname()
        self._port = 5000
        self._socket.bind((self._host, self._port))
        self._shutdown = False

        self._threads = {}

        self._socket.listen(20)

        self.run()

    def run(self):

        while not self._shutdown:
            client, address = self._socket.accept()
            print('Got connection from', address)
            print()

            client_name = client.recv(1024).decode()
            client.close()

            print("Matrix 1")
            matrix_1 = self.recv_matrix()

            print("Matrix 2")
            matrix_2 = self.recv_matrix()

            self.send_final_ack()

            thread_1_id = "TH1_" + client_name
            thread_2_id = "TH2_" + client_name

            self._threads[thread_1_id] = self.ProcessingThread(thread_1_id, MATRIX_MULTIPLIER_THREAD, matrix_1, matrix_1)
            self._threads[thread_1_id].start()

            self._threads[thread_2_id] = self.ProcessingThread(thread_2_id, MATRIX_ADDER_THREAD, matrix_1, matrix_2)
            self._threads[thread_2_id].start()

    def recv_matrix(self):
        client, address = self._socket.accept()
        data = client.recv(1024).decode()

        print(data)
        print()

        client.close()

        rows = data.split("\n")
        matrix = [[int(x) for x in row.split()] for row in rows]

        return matrix

    def send_final_ack(self):
        client, address = self._socket.accept()
        client.send('Thank you for connecting'.encode())
        client.close()

    @staticmethod
    def matrix_multiply(matrix_1, matrix_2):
        print("Multiplying")

    @staticmethod
    def matrix_add(matrix_1, matrix_2):
        print("Adding")

    class ProcessingThread(threading.Thread):

        def __init__(self, thread_id, thread_type, matrix_1, matrix_2):
            threading.Thread.__init__(self)
            self._thread_id = thread_id
            self._thread_type = thread_type
            self._matrix_1 = matrix_1
            self._matrix_2 = matrix_2

        def run(self):
            print("Starting " + self.name)
            self.execute()
            print("Exiting " + self.name)

        def execute(self):
            print("%s, %s : %s" % (self._thread_id, self._thread_type, time.ctime(time.time())))

            if self._thread_type is MATRIX_MULTIPLIER_THREAD:
                Server.matrix_multiply(self._matrix_1, self._matrix_2)
            else:
                if self._thread_type is MATRIX_ADDER_THREAD:
                    pass
                    Server.matrix_add(self._matrix_1, self._matrix_2)

