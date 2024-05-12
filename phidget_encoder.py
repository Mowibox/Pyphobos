from Phidget22.Phidget import *
from Phidget22.Devices.Encoder import *
from robot_config import *
import numpy as np
import time



def encoder_init(serial_number, hub_port):
	encoder = Encoder()
	encoder.setHubPort(hub_port)
	encoder.setDeviceSerialNumber(serial_number)
	encoder.openWaitForAttachment(5000)

	return encoder

def updatePosition(encoder_left, encoder_right, x, y, theta):
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


encoder_left = encoder_init(serial_number, encoder_left_hub_port)
encoder_right = encoder_init(serial_number, encoder_right_hub_port)

try:	
	while True:
		(x,y,theta) = updatePosition(encoder_left, encoder_right, 0, 0, 0)
		print(f"x: {round(x, 2)} mm, y: {round(y, 2)} mm, theta : {round(theta*180/np.pi, 2)}°")

except (Exception, KeyboardInterrupt):
	pass
	encoder_left.close()
	encoder_right.close()
encoder_left.close()
encoder_right.close()

