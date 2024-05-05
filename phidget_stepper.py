from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from robot_config import *
from lidar_vl53l1x import *
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

def move_forward(stepper_left, stepper_right, lidar_data, serial, speed, distance):
    speed_factor = 1.0
    step = distance / (2 * np.pi * WHEEL_RADIUS)
    stepper_left.setTargetPosition(step)
    stepper_right.setTargetPosition(-step)
    while abs(distance / 260 - stepper_left.getPosition()) >= 1e-2:
        lidar_data.rx_storage = serial.read(LIDAR_FRAME_SIZE * 2)
        processed_data = get_lidar_data(lidar_data)
        distances = [distance[1] for distance in processed_data.measure]
        min_distance = min(distances)
        min_distance_index = distances.index(min_distance) 
        if min_distance_index in [0, 1, 7, 8, 9, 10, 14, 15]:
            threshold = 140
        else:
            threshold = 310
        if 1 <= min_distance <= threshold:
            speed_factor = 0.0
        elif min_distance >= threshold:
            speed_factor = 1-np.exp(-(min_distance-threshold)/25)
            
        stepper_left.setVelocityLimit(speed * speed_factor)
        stepper_right.setVelocityLimit(speed * speed_factor)
        time.sleep(0.001)
    stepper_left.addPositionOffset(-stepper_left.getPosition())
    stepper_right.addPositionOffset(-stepper_right.getPosition())
    stepper_left.setVelocityLimit(0)
    stepper_right.setVelocityLimit(0)
    return


def rotate_left(stepper_left, stepper_right, speed, theta):
	speed_factor = 1.0
	distance = np.pi*WHEEL_ENTRAXE*theta/360
	stepper_left.setVelocityLimit(speed*speed_factor)
	stepper_right.setVelocityLimit(speed*speed_factor)
	step = distance/(2*np.pi*WHEEL_RADIUS)
	stepper_left.setTargetPosition(-step/2)
	stepper_right.setTargetPosition(-step/2)
	time.sleep(1.5)
	stepper_left.addPositionOffset(-stepper_left.getPosition())
	stepper_right.addPositionOffset(-stepper_right.getPosition())
	return