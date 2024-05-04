from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time


def stepper_init(serial_number, hub_port, rescale_factor=1/3200):
	stepper = Stepper()
	stepper.setDeviceSerialNumber(serial_number)
	stepper.setHubPort(hub_port)
	stepper.openWaitForAttachment(5000)
	stepper.setRescaleFactor(rescale_factor)
	stepper.setControlMode(StepperControlMode.CONTROL_MODE_STEP)
	stepper.setCurrentLimit(3)
	return stepper

stepper_left = stepper_init(723793, 5)
stepper_right = stepper_init(723793, 0)

stepper_left.setTargetPosition(1)
stepper_right.setTargetPosition(-1)
stepper_left.setEngaged(True)
stepper_right.setEngaged(True)

try:
	input("Press Enter to Stop\n")
except (Exception, KeyboardInterrupt):
	pass

stepper_left.close()
stepper_right.close()

