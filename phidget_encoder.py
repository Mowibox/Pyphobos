"""
    @file        phidget_encoder.py
    @author      Mowibox (Ousmane THIONGANE)
    @brief       File to use a Phidget Encoder
    @version     1.0
    @date        2024-05-04
    
"""

from Phidget22.Phidget import *
from Phidget22.Devices.Encoder import *
from robot_config import *
import numpy as np
import time



def encoder_init(serial_number: int, hub_port: int) -> Encoder:
	"""
	Initialization of a Phidgets Encoder

	@param serial_number: The serial number of the Phidget Hub
	@param hub_port: The port hub of the encoder on the Phidget Hub
	"""
	encoder = Encoder()
	encoder.setHubPort(hub_port)
	encoder.setDeviceSerialNumber(serial_number)
	encoder.openWaitForAttachment(5000)

	return encoder

def updatePosition(encoder_left: Encoder, encoder_right: Encoder, x: float, y: float, theta: float) -> tuple[float, float, float]:
	"""
	Update the position of the robot on a (x, y, theta) coordinates.

	@param encoder_left: The left encoder
	@param encoder_right: The right encoder
	@param x: Horizontal axis (mm)
	@param y: Vertical axis (mm)
	@param theta: Robot angle (rad)
	"""
	K = (2*np.pi*ODOMETRY_RADIUS/TICKS_PER_REV)
	left_mov = K*encoder_left.getPosition()
	right_mov = -K*encoder_right.getPosition()

	r = (left_mov + right_mov)/2
	alpha = (left_mov - right_mov)/ODOMETRY_ENTRAXE
	dx = r*np.cos(theta + alpha/2)
	dy = r*np.sin(theta + alpha/2)

	x += dx
	y += dy
	theta += alpha

	if theta > np.pi:
		theta -= 2*np.pi
	elif theta < -np.pi:
		theta += 2*np.pi
	return x, y, theta


# Initializing encoders
encoder_left = encoder_init(serial_number, encoder_left_hub_port)
encoder_right = encoder_init(serial_number, encoder_right_hub_port)

# Debug
(x, y, theta) = (0, 0, 0)
digit_precision = 2
try:	
	while True:
		(x, y, theta) = updatePosition(encoder_left, encoder_right, x, y, theta)
		print(f"x: {round(x, digit_precision)} mm, y: {round(y, digit_precision)} mm, theta : {round(theta*180/np.pi, digit_precision)}°")

except (Exception, KeyboardInterrupt):
	encoder_left.close()
	encoder_right.close()
	pass