from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from robot_config import *
import time
import numpy as np


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
	return
	

stepper_left = stepper_init(723793, 5)
stepper_right = stepper_init(723793, 0)



try:
	input("Press Enter to Stop\n")
except (Exception, KeyboardInterrupt):
	pass

stepper_left.close()
stepper_right.close()

