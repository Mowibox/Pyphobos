from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time
import numpy as np
import serial
import serial.tools.list_ports
import RPi.GPIO as GPIO
from phidget_stepper import *


def strategy(strategy_number, stepper_left, stepper_right, lidar_data, serial):
    if strategy_number == 0:
        pass
    elif strategy_number == 1:
        pass
    elif strategy_number == 2:
        pass
    elif strategy_number == 3:
        pass
    elif strategy_number == 4:
        pass
    elif strategy_number == 5:
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 1200)
        time.sleep(1)
        speed = 2
        rotate_left(stepper_left, stepper_right, speed, 90)
        time.sleep(0.5)
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -600)
        time.sleep(1)
        speed = 2
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 600)
        time.sleep(1)
        rotate_left(stepper_left, stepper_right, speed, -270)
        time.sleep(0.5)
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 1200)
    return





