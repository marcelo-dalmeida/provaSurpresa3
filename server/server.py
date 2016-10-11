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


            thread_1_id = "TH1_" + client_name
            thread_2_id = "TH2_" + client_name
            
            self._threads[thread_1_id] = self.ProcessingThread(thread_1_id, MATRIX_MULTIPLIER_THREAD, matrix_1, matrix_1)
            self._threads[thread_1_id].start()
            
            self._threads[thread_2_id] = self.ProcessingThread(thread_2_id, MATRIX_ADDER_THREAD, matrix_1, matrix_2)
            self._threads[thread_2_id].start()
            
            self.send_final_ack(client_name)
            self._shutdown = True

    def recv_matrix(self):
        client, address = self._socket.accept()
        data = client.recv(1024).decode()

        print(data)
        print()

        client.close()

        rows = data.split("\n")
        matrix = [[int(x) for x in row.split()] for row in rows]

        return matrix

    def send_final_ack(self, client_name):
        client, address = self._socket.accept()
        #print("awfawef: "+str(client_name))
        #matrix_file = open("soma-TH2_" + str(client_name) + ".txt", "rb")
        #matrix = matrix_file.read(1024)
        #self._socket.send(matrix)
        #matrix_file = open("multiplica-TH1_" + str(client_name) + ".txt", "rb")
        #matrix = matrix_file.read(1024)
        #self._socket.send(matrix)
        client.send('Thank you for connecting'.encode())
        client.close()

    @staticmethod
    def matrix_multiply(matrix_1, matrix_2, thr_id):
        f = open('multiplica-' + str(thr_id) + '.txt', 'w')
        print("Multiplying...")
        m_index = int(len(matrix_1[0]))
        m = [[0 for x in range(m_index+1)] for y in range(m_index+1)]
        for i in range(0,m_index):
            for j in range(0,m_index):
                s = 0
                for k in range(0,m_index):
                    s = s + matrix_1[i][j] * matrix_2[j][i]
                m[i][j] = s
                f.write(str(m[i][j]) + " ")
                #print(m[i][j], end=" ")
            f.write("\n")
            #print()
        f.close()
        

    @staticmethod
    def matrix_add(matrix_1, matrix_2, thr_id):
        f = open('soma-' + str(thr_id) + '.txt', 'w')
        print("Adding...")
        m_index = int(len(matrix_1[0]))
        m = [[0 for x in range(m_index+1)] for y in range(m_index+1)]
        for i in range(0,m_index):
            for j in range(0,m_index):
                m[i][j] = matrix_1[i][j] + matrix_2[i][j]
                f.write(str(m[i][j]) + " ")
                #print(m[i][j], end=" ")
            f.write("\n")
            #print()
        f.close()
    
    @staticmethod
    def convert_time(time_ms):
        s, ms = divmod(start, 60)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        h = h%24
        return("%dh%02dmin%02ds0%dms" % (h, m, s, ms))
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
                Server.matrix_multiply(self._matrix_1, self._matrix_2, self._thread_id)
            else:
                if self._thread_type is MATRIX_ADDER_THREAD:
                    pass
                    Server.matrix_add(self._matrix_1, self._matrix_2, self._thread_id)

server_node = Server()
