from robot_config import *
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time
import numpy as np
import serial
import serial.tools.list_ports
import RPi.GPIO as GPIO
from phidget_stepper import *
import sys
import threading
from strategy import *


def stop_program():
    time.sleep(10)  
    stepper_left.close()
    stepper_right.close()
    GPIO.cleanup()
    sys.exit()

def find_screen_port():
    stlink_ports = [port.device for port in serial.tools.list_ports.comports() if "ST-Link" in port.description]
    if stlink_ports:
        return stlink_ports[0]
    else:
        return None


port = find_screen_port() 
baudrate = 115200  
timeout = 1

if port:
    ser = serial.Serial(port, baudrate, timeout=timeout)
else: 
    print("No screen device found on target !")
    exit()

while True:
    received_data = ser.readline().decode().strip()
    if len(received_data) != 0:
        strategy_number = int(received_data)
        break
ser.close()

stepper_left = stepper_init(serial_number, left_hub_port)
stepper_right = stepper_init(serial_number, right_hub_port)

GPIO.setmode(GPIO.BCM)
GPIO.setup(start_pin, GPIO.IN)
previous_state = GPIO.input(start_pin)

while True:
    current_state = GPIO.input(start_pin)
    
    if current_state != previous_state:
        # print(strategy)
        break
    time.sleep(0.1)


ser1 = serial.Serial("/dev/ttyAMA1", baudrate=115200, timeout=5.0)
lidar_data = AresLidar()

timer_thread = threading.Thread(target=stop_program)
timer_thread.start()

strategy(strategy_number, stepper_left, stepper_right)

timer_thread.join()

stepper_left.close()
stepper_right.close()
GPIO.cleanup()
