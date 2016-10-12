import threading
import time
import datetime
import server_side.util as util

class ProcessingThread(threading.Thread):

    def __init__(self, thread_id, thread_type, matrix_1, matrix_2, notifier):
        threading.Thread.__init__(self)
        self._thread_id = thread_id
        self._thread_type = thread_type
        self._matrix_1 = matrix_1
        self._matrix_2 = matrix_2
        self._result_matrix_filename = None

        self._notifier = notifier

        self._thread_start_time = 0
        self._thread_finish_time = 0


    def start(self):

        thread = threading.Thread.start(self)

    def run(self):
        self._thread_start_time = datetime.datetime.now()
        print("Starting " + self.name)
        self.execute()
        print("Exiting " + self.name)
        self._thread_finish_time = datetime.datetime.now()
        self._notifier.notify(self._thread_id, self._result_matrix_filename, self._thread_start_time, self._thread_finish_time)


    def execute(self):
        print("%s, %s : %s" % (self._thread_id, self._thread_type, time.ctime(time.time())))

        if self._thread_type is util.MATRIX_MULTIPLIER_THREAD:

            self.matrix_multiply(self._matrix_1, self._matrix_2)
        else:
            if self._thread_type is util.MATRIX_ADDER_THREAD:
                self.matrix_add(self._matrix_1, self._matrix_2)


    def matrix_multiply(self, matrix_1, matrix_2):
        self._result_matrix_filename = 'multiplica-' + self._thread_id + '.txt'
        result_matrix_file = open(util.OUTPUT_FOLDER + self._result_matrix_filename, 'w')
        print("Multiplying...")
        matrix_size = len(matrix_1)

        for i in range(matrix_size):
            for j in range(matrix_size):
                number = 0
                for k in range(matrix_size):
                    number += matrix_1[i][k] * matrix_2[k][j]
                result_matrix_file.write(str(number) + "\t")
            if i != matrix_size - 1:
                result_matrix_file.write("\n")

        result_matrix_file.close()

    def matrix_add(self, matrix_1, matrix_2):
        self._result_matrix_filename = 'soma-' + self._thread_id + '.txt'
        result_matrix_file = open(util.OUTPUT_FOLDER + self._result_matrix_filename, 'w')
        print("Adding...")

        matrix_size = len(matrix_1)
        for i in range(matrix_size):
            for j in range(matrix_size):
                number = matrix_1[i][j] + matrix_2[i][j]
                result_matrix_file.write(str(number) + "\t")
            if i != matrix_size - 1:
                result_matrix_file.write("\n")
        result_matrix_file.close()
