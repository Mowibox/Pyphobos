from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from phidget_stepper import *
import time


speed = 2

def elevator(stepper_elevator, level):
	step = level
	stepper_elevator.setTargetPosition(step)
	while abs(level/260 - stepper_elevator.getPosition()) >= 1e-2:
		stepper_elevator.setVelocityLimit(speed*speed_factor)
		stepper_right.setVelocityLimit(speed*speed_factor)
		time.sleep(0.1)
	stepper_elevator.addPositionOffset(-stepper_elevator.getPosition())
	stepper_elevator.setVelocityLimit(0)
	return


stepper_elevator = stepper_init(723793, 0)
elevator(stepper_left, stepper_right, 2)