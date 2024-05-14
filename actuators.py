"""
    @file        actuators.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       Actuators file for the French Robotics Cup 2024
    @version     1.0
    @date        2024-05-04
    
"""
# Includes
from Phidget22.Devices.Stepper import *
from Phidget22.Phidget import *
from robot_config import *
import RPi.GPIO as GPIO
import time


# PWM pin start
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  


def elevator(stepper_elevator: Stepper, level: float):
	"""
	A function to operate the plant elevator

	@param The elevator stepper
	@param level: The height level of the elevator (on %) 
    """
	step = level*22/100
	stepper_elevator.setVelocityLimit(1.5)
	stepper_elevator.setTargetPosition(step)
	stepper_elevator.addPositionOffset(-stepper_elevator.getPosition())
	stepper_elevator.setVelocityLimit(0)
	return


def turnstile(stepper_turnstile: Stepper, rotation_step: int):
	"""
	A function to rotate the pot turnstile

    @param stepper_turnstile: The turnstile stepper
	@param rotation_step: Rotation step of the turnstile
    """
	step = rotation_step*22/100
	stepper_turnstile.setVelocityLimit(0.5)
	stepper_turnstile.setTargetPosition(step)
	stepper_turnstile.addPositionOffset(-stepper_turnstile.getPosition())
	stepper_turnstile.setVelocityLimit(0)
	return


def set_angle(angle: float):
    """
	Function to give an angle to a servo motor:

	@param angle: Angle position goal
    """
    duty_cycle = (angle / 18) + 2 # Angle to duty cycle conversion
    pwm.start(duty_cycle)
    time.sleep(1)
    return



