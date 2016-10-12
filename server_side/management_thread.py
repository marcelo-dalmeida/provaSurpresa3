import threading
import datetime
import socket
from server_side.processing_thread import ProcessingThread
from server_side.notifier import Notifier
import server_side.util as util


class ManagementThread(threading.Thread):

        def __init__(self, port):
            threading.Thread.__init__(self)
            self._threads = {}
            self._filenames = {}
            self._start_times = {}
            self._finish_times = {}

            self._socket = socket.socket()
            host = socket.gethostname()
            self._socket.bind((host, port))

            self._socket.listen()

            self._thread_1_id = None
            self._thread_2_id = None

            self._notifier = Notifier(self)

        def start(self):
            threading.Thread.start(self)

        def run(self):
            print("Starting " + self.name)
            self.execute()
            print("Exiting " + self.name)

        def execute(self):

            client, address = self._socket.accept()
            print('Got connection from', address)
            print()
            #print("%s, %s : %s" % (self._thread_id, self._thread_type, time.ctime(time.time())))

            client_name = client.recv(1024).decode()
            client.close()

            print("Matrix 1")
            matrix_1 = self.recv_matrix()

            print("Matrix 2")
            matrix_2 = self.recv_matrix()

            self._thread_1_id = "TH1_" + client_name
            self._thread_2_id = "TH2_" + client_name

            self._threads[self._thread_1_id] = ProcessingThread(self._thread_1_id, util.MATRIX_MULTIPLIER_THREAD, matrix_1, matrix_1, self._notifier)
            self._threads[self._thread_1_id].start()

            self._threads[self._thread_2_id] = ProcessingThread(self._thread_2_id, util.MATRIX_ADDER_THREAD, matrix_1, matrix_2, self._notifier)
            self._threads[self._thread_2_id].start()

            self._threads[self._thread_1_id].join()
            self._threads[self._thread_2_id].join()


            for thread_id in self._threads.keys():
                self.send_matrix(self._filenames[thread_id])
                self.send_time(self._start_times[thread_id], self._finish_times[thread_id])

            self.send_final_ack()

        def recv_matrix(self):
            client, address = self._socket.accept()

            data = ""
            matrix = client.recv(1024).decode()
            while (matrix):
                data += matrix
                matrix = client.recv(1024).decode()
            print(data)
            print()

            client.close()

            rows = data.split("\n")
            matrix = [[int(x) for x in row.split()] for row in rows]

            return matrix

        def send_matrix(self, matrix_filename):
            client, address = self._socket.accept()
            matrix_file = open(util.OUTPUT_FOLDER + matrix_filename, "rb")

            matrix = matrix_file.read(1024)
            while matrix:
                client.send(matrix)
                matrix = matrix_file.read(1024)

            client.close()

        def send_time(self, start_time, finish_time):
            total_time = finish_time - start_time
            total_time = datetime.time(microsecond=total_time.microseconds)

            client, address = self._socket.accept()
            client.send(util.convert_time(start_time).encode())
            client.close()

            client, address = self._socket.accept()
            client.send(util.convert_time(finish_time).encode())
            client.close()

            client, address = self._socket.accept()
            client.send(util.convert_time(total_time).encode())
            client.close()


        def send_final_ack(self):
            client, address = self._socket.accept()
            client.send('Thank you for connecting'.encode())
            client.close()


        def notify(self, thread_id, matrix_filename, start_time, finish_time):
            self._filenames[thread_id] = matrix_filename
            self._start_times[thread_id] = start_time
            self._finish_times[thread_id] = finish_time


