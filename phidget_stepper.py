from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from robot_config import *
import time
import numpy as np

WHEEL_RADIUS = 41.436
ENTRAXE = 240
speed = 1
speed_factor = 1.0

def stepper_init(serial_number, hub_port, rescale_factor=1/3200):
	stepper = Stepper()
	stepper.setDeviceSerialNumber(serial_number)
	stepper.setHubPort(hub_port)
	stepper.openWaitForAttachment(5000)
	stepper.setRescaleFactor(rescale_factor)
	stepper.setControlMode(StepperControlMode.CONTROL_MODE_STEP)
	stepper.setCurrentLimit(3)
	stepper.setEngaged(True)

	return stepper


def move_forward(stepper_left, stepper_right, distance):
	step = distance/(2*np.pi*WHEEL_RADIUS)
	stepper_left.setTargetPosition(step)
	stepper_right.setTargetPosition(-step)
	while abs(distance/260 - stepper_left.getPosition()) >= 1e-2:
		stepper_left.setVelocityLimit(speed*speed_factor)
		stepper_right.setVelocityLimit(speed*speed_factor)
		time.sleep(0.1)
	stepper_left.addPositionOffset(-stepper_left.getPosition())
	stepper_right.addPositionOffset(-stepper_right.getPosition())
	stepper_left.setVelocityLimit(0)
	stepper_right.setVelocityLimit(0)
	return
	


def rotate_left(stepper_left, stepper_right, theta):
	distance = np.pi*ENTRAXE*theta/360
	stepper_left.setVelocityLimit(speed*speed_factor)
	stepper_right.setVelocityLimit(speed*speed_factor)
	step = distance/(2*np.pi*WHEEL_RADIUS)
	stepper_left.setTargetPosition(-step/2)
	stepper_right.setTargetPosition(-step/2)
	time.sleep(1.5)
	stepper_left.addPositionOffset(-stepper_left.getPosition())
	stepper_right.addPositionOffset(-stepper_right.getPosition())
	return

stepper_left = stepper_init(723793, 5)
stepper_right = stepper_init(723793, 0)

rotate_left(stepper_left, stepper_right, 45)
time.sleep(1)
move_forward(stepper_left, stepper_right, 600)
time.sleep(1)
rotate_left(stepper_left, stepper_right, 90)
time.sleep(1)
move_forward(stepper_left, stepper_right, 1200)

try:
	input("Press Enter to Stop\n")
except (Exception, KeyboardInterrupt):
	pass

stepper_left.close()
stepper_right.close()

