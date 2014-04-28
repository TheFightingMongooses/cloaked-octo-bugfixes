import os, json
import serial
from serial.tools import list_ports
import pickle
import numpy as np
import udp_listen
from udp_listen import set_next_waypoint, get_robit_position
from math import atan2, degrees, pi

COLOR_MAP = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'purple',
    4: 'yellow'
}

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
    values = serial_string.split('\t')
    labels = ['left_sharp', 'right_sharp', 'sharp_top', 'red', 'green', 'blue']
    try:
        return {label: int(value) for label, value in zip(labels, values)}
    except ValueError:
        return None 

def think_motors(brain_dict, margin=500):
    velocity, direction = ('40', '0')
    if brain_dict and 'left_sharp' in brain_dict.keys() and 'right_sharp' in brain_dict.keys():
        if brain_dict['left_sharp'] > margin and brain_dict['right_sharp'] > margin:
            velocity, direction = ('40', '180')
        elif brain_dict['left_sharp'] > margin:
            velocity, direction = ('40', '215')
        elif brain_dict['right_sharp'] > margin:
            velocity, direction = ('40', '135')
    return velocity, direction

def color_vector(brain_dict):
    return [
        brain_dict['red'],
        brain_dict['green'],
        brain_dict['blue']
    ]

def think_servos(brain_dict):
    return ('45', '45')

def messages(brain_dict, margin=500):
    if brain_dict:
        if brain_dict['left_sharp'] > margin and brain_dict['right_sharp'] > margin:
            print "STOP, RUN AWAY"
        elif brain_dict['left_sharp'] > margin:
            print "PIVOT RIGHT"
        elif brain_dict['right_sharp'] > margin:
            print "PIVOT LEFT"

def check_color_detect(detector="knn", ser=setup_serial()):
    clf = pickle.load(open('%s.pkl' % detector, 'r'))
    while True:
        newline = ser.readline()
        brain_dict = brain(newline)
        try:
            print clf.predict(np.array(color_vector(brain_dict)))
        except (KeyError, TypeError):
            pass

def calc_direction(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    rads = atan2(-dy,dx)
    rads %= 2*pi
    return degrees(rads) 

def do_robot_things():
    set_next_waypoint()
    last_position = False
    current_heading = False
    desired_heading = False
    while True:
        new_position = get_robit_position()
        desired_heading = calc_direction(new_position, udp_listen.CURRENT_GOAL)
        if last_position:
            current_heading = calc_direction(last_position, new_position)
        last_position = new_position
        if desired_heading and current_heading:
            print current_heading, desired_heading

if __name__ == '__main__':
    do_robot_things()    


