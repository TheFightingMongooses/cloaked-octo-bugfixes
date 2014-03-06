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

if __name__ == '__main__':
    ser = setup_serial()
    while True:
        print ser.readline()
        print "~~~~"
