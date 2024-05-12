"""
    @file        strategy.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       
    @version     1.0
    @date        2024-
    
"""
# Includes
from Phidget22.Devices.Stepper import *
from Phidget22.Phidget import *
from phidget_stepper import *
from actuators import *
import numpy as np
import time
import serial
import serial.tools.list_ports


def strategy(strategy_number, stepper_left, stepper_right, lidar_data, serial):
    if strategy_number == 0:
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 700)
        time.sleep(1)
        speed = 2
        rotate_left(stepper_left, stepper_right, speed, 90)
        time.sleep(0.5)
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -700)
        speed = 2
        rotate_left(stepper_left, stepper_right, speed, -270)
        time.sleep(0.5)
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -700)
        time.sleep(1)
        speed = 2
        rotate_left(stepper_left, stepper_right, speed, -135)
        time.sleep(0.5)
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, np.sqrt(2)*700)
        time.sleep(1)
        rotate_left(stepper_left, stepper_right, speed, -45)
        time.sleep(0.5)
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -700)
        

    elif strategy_number == 1:
        speed = 0.3
        rotate_left(stepper_left, stepper_right, speed, 360*5) 


    elif strategy_number == 2:
        pass


    elif strategy_number == 3:
        speed = 0.3
        for i in range(8):
            rotate_left(stepper_left, stepper_right, speed, -90)


    elif strategy_number == 4:
        set_angle(80)
        speed = 1.5
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -510)
        time.sleep(0.5)
        speed = 0.8
        #move_forward(stepper_left, stepper_right,
         #lidar_data, serial, speed, -1000)
        #time.sleep(1)
        #set_angle(0)
        #speed = 1.1
        #move_forward(stepper_left, stepper_right,
        # lidar_data, serial, speed, 1000)
        #time.sleep(0.5)
        speed = 1
        rotate_left(stepper_left, stepper_right, speed,  -35.5)
        time.sleep(1)
        speed = 0.8
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -510)
        set_angle(0)
        pwm.stop()
        time.sleep(1)
        speed = 0.45
        rotate_left(stepper_left, stepper_right, speed, -93.5)
        time.sleep(0.5)
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -1320)
        time.sleep(0.5)
        rotate_left(stepper_left, stepper_right, speed, -28.5)
        time.sleep(1)
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -250)
        time.sleep(0.5)
        speed = 1.2
        #move_forward(stepper_left, stepper_right,
        # lidar_data, serial, speed, 1200)
        speed = 1.2
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 325)
        speed = 0.8
        rotate_left(stepper_left, stepper_right, speed, 45)
        # speed = 1
        # rotate_left(stepper_left, stepper_right, speed, 180-20)
        # speed = 1.5
        # move_forward(stepper_left, stepper_right,
        # lidar_data, serial, speed, 1500)
        # time.sleep(1)
        # rotate_left(stepper_left, stepper_right, speed, -(180-43))


    elif strategy_number == 5:
        speed = 0.8
        #move_forward(stepper_left, stepper_right,
        # lidar_data, serial, speed, 100)
        #time.sleep(1)
        #set_angle(105)
        #speed = 0.35
        #move_forward(stepper_left, stepper_right,
        # lidar_data, serial, speed, -100)
        #time.sleep(0.5)
        #speed = 0.8
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 100)
        set_angle(85)
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 430)
        set_angle(0)
        pwm.stop()
        rotate_left(stepper_left, stepper_right, speed, -132)
        time.sleep(1)
        speed = 0.55
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -467)
        time.sleep(1)
        speed = 0.22
        rotate_left(stepper_left, stepper_right, speed, 65)
        """
        speed = 1
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 0.1*np.sqrt(1050**2+1350**2))
        """
        # rotate_left(stepper_left, stepper_right, speed, 20)
        speed = 0.6
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, -1326)
        time.sleep(1)
        move_forward(stepper_left, stepper_right,
         lidar_data, serial, speed, 310)
        rotate_left(stepper_left, stepper_right, speed, -26)
    return





