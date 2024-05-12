"""
    @file        actuators.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       
    @version     1.0
    @date        2024-
    
"""
# Includes
from Phidget22.Devices.Stepper import *
from Phidget22.Phidget import *
from robot_config import *
import RPi.GPIO as GPIO
import time


# Servo PWM pin start
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  


def elevator(stepper_elevator: Stepper, level: float):
	"""
    """
	step = level*22/100
	stepper_elevator.setVelocityLimit(1.5)
	stepper_elevator.setTargetPosition(step)
	stepper_elevator.addPositionOffset(-stepper_elevator.getPosition())
	stepper_elevator.setVelocityLimit(0)
	return


def turnstile(stepper_turnstile: Stepper, rotation_step: int):
	"""
    """
	step = rotation_step*22/100
	stepper_turnstile.setVelocityLimit(0.5)
	stepper_turnstile.setTargetPosition(step)
	stepper_turnstile.addPositionOffset(-stepper_turnstile.getPosition())
	stepper_turnstile.setVelocityLimit(0)
	return


def set_angle(angle: float):
    """
    """
    duty_cycle = (angle / 18) + 2
    pwm.start(duty_cycle)
    time.sleep(1)
    return



