"""
    @file        main_phobos.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       
    @version     1.0
    @date        2024-
    
"""

# Includes
from Phidget22.Devices.Stepper import *
from Phidget22.Phidget import *
import serial.tools.list_ports
from phidget_stepper import *
from robot_config import *
import RPi.GPIO as GPIO
from actuators import *
from strategy import *
import numpy as np
import threading
import serial
import time

# Using LED to checkout if the robot boots well
checkout_led = 11

strategy_led = 6

def stop_program():
    """
    Timer to stop the robot at the end of the match
    """
    time.sleep(90)
    GPIO.output(checkout_led, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()  
    ser_lidar.close()
    stepper_left.close()
    stepper_right.close()
    exit()


def find_screen_port():
    """
    Search the ST-Link port used for the screen
    """
    stlink_ports = [port.device for port in serial.tools.list_ports.comports() if "ST-Link" in port.description]
    if stlink_ports:
        return stlink_ports[0]
    else:
        return None



# Main code
try:
    time.sleep(2)
    # Checkout LED Toggle
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(checkout_led, GPIO.OUT)
    GPIO.output(checkout_led, GPIO.HIGH)
    GPIO.setup(strategy_led, GPIO.IN)

    # Configuring screen serial communication
    # port = find_screen_port() 
    # baudrate = 115200  
    # timeout = 1

    # if port:
    #     ser_screen = serial.Serial(port, baudrate, timeout=timeout)
    # else: 
    #     print("No screen device found on target !")
    #     exit()


    # Reading the incoming strategy
    # while True:
    #     received_data = ser_screen.readline().decode().strip()
    #     if len(received_data) != 0:
    #         strategy_number = int(received_data)
    #         break
    # ser_screen.close()

    # Initializing steppers
    stepper_left = stepper_init(serial_number, left_hub_port)
    stepper_right = stepper_init(serial_number, right_hub_port)

    # Configuring start pull pin
    GPIO.setup(start_pin, GPIO.IN)
    previous_state = GPIO.input(start_pin)

    while True:
        current_state = GPIO.input(start_pin)
        if current_state != previous_state:
            GPIO.output(checkout_led, GPIO.LOW)
            break
        time.sleep(0.1)    

    if GPIO.input(strategy_led) == 1:
        strategy_number = 5
    else:
        strategy_number = 4
    print(strategy_number)
    # Configuring lidar serial communication 
    ser_lidar = serial.Serial("/dev/ttyAMA1", baudrate=115200, timeout=5.0)
    lidar_data = AresLidar()

    # Starting the match timer in a thread
    timer_thread = threading.Thread(target=stop_program)
    timer_thread.start()

    # Running the robot strategy
    strategy(strategy_number, stepper_left, stepper_right, lidar_data, ser_lidar)

    # Closing parameters
    ser_lidar.close()
    stepper_left.close()
    stepper_right.close()
    timer_thread.close()
    GPIO.cleanup()
    exit()

except (Exception, KeyboardInterrupt):
    GPIO.cleanup()
    if stepper_left != None:
        stepper_left.close()
    if stepper_right != None:
        stepper_right.close()
    if timer_thread != None:
        timer_thread.join()
    if ser_lidar != None:
        ser_lidar.close()
    exit()

