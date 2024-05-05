from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from phidget_stepper import stepper_init
import RPi.GPIO as GPIO
import time

speed_factor = 1.0
speed = 2

def elevator(stepper_elevator, level):
	step = level*22/100
#	stepper_elevator.setVelocityLimit(2)
	stepper_elevator.setTargetPosition(step)
	#while abs(level/260 - stepper_elevator.getPosition()) >= 1e-1:
	#	print(stepper_elevator.getPosition())
	#	stepper_elevator.setVelocityLimit(speed*speed_factor)
	#	time.sleep(0.1)
	stepper_elevator.addPositionOffset(-stepper_elevator.getPosition())
	stepper_elevator.setVelocityLimit(0)
	return

servo_pin = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM configuration
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz

def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2
    return duty_cycle

def set_angle(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1)  
    pwm.stop()

# stepper_elevator = stepper_init(723793, 0)
# elevator(stepper_elevator, -50)
set_angle(135)

try:
	input("Press Enter to Stop\n")
except (Exception, KeyboardInterrupt):
	pass

# stepper_elevator.close()



set_angle(135)
time.sleep(3)
set_angle(0)

GPIO.cleanup()
