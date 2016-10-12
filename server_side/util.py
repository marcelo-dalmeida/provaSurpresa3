__author__ = 'Marcelo d\'Almeida'

MATRIX_ADDER_THREAD = "Matrix Adder Thread"
MATRIX_MULTIPLIER_THREAD = "Matrix Multiplier Thread"
OUTPUT_FOLDER = "../files/output/"

def convert_time(datetime_value):
    #print(datetime_value.strftime("%Hh%Mm%Ss%fus"))
    h_m_s = datetime_value.strftime("%Hh%Mm%Ss")
    ms = datetime_value.strftime("%f")[:-3] + "ms"
    us = datetime_value.strftime("%fus")[3:]
    date_time_formatted = h_m_s + ms + us
    #print(date_time_formatted)
    return date_time_formatted
