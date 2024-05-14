"""
    @file        robot_config.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Configuration file containing the main parameters of the robot
    @version     1.0
    @date        2024-05-04
    
"""

# Wheel parameters
WHEEL_RADIUS = 41.436
WHEEL_ENTRAXE = 111

# Odometry parameters
ODOMETRY_RADIUS = 26.9811
ODOMETRY_ENTRAXE = 240
TICKS_PER_REV = 8192

# GPIO pins 
start_pin = 26
servo_pin = 19

# Phidget parameters
serial_number = 723793
stepper_left_hub_port = 5
stepper_right_hub_port = 0

elevator_hub_port = 2
turnstile_hub_port = 3

encoder_left_hub_port = 4
encoder_right_hub_port = 1

