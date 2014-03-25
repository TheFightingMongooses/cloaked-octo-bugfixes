import os
import serial
from serial.tools import list_ports


def find_uart_port():
    for port in list_ports.comports():
        if port[1] == 'FT232R USB UART':
            return port[0]
    raise ValueError

def setup_serial(baud=38400):
    return serial.Serial(find_uart_port(), baud)

def determine_color(color_vector):
	"""
	Right now just a stub, but will totally collect some data and smack an svm in here
	"""
	return 'Red'

def brain(serial_string):
	values = serial_string.split('`')
	return [int(value) for value in values[-3:]]


if __name__ == '__main__':
    ser = setup_serial()
    with open('red.txt', 'a') as sink:
        while True:
            newline = ser.readline()
            #sink.write(",".join(brain(newline)) + "\n")
            print newline
            print "~~~~"
