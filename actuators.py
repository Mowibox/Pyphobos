from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import RPi.GPIO as GPIO
import time
from robot_config import *



GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  


def elevator(stepper_elevator, level):
	step = level*22/100
	stepper_elevator.setVelocityLimit(1.5)
	stepper_elevator.setTargetPosition(step)
	stepper_elevator.addPositionOffset(-stepper_elevator.getPosition())
	stepper_elevator.setVelocityLimit(0)
	return

def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2
    return duty_cycle


def set_angle(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1)  
    pwm.stop()
