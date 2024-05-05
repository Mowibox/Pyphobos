from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time
import numpy as np
import serial
import serial.tools.list_ports
import RPi.GPIO as GPIO
from phidget_stepper import *

WHEEL_RADIUS = 41.436
ENTRAXE = 240
LIDAR_MODULE_NUMBER = 16
LIDAR_FRAME_SIZE = 114
speed = 1
speed_factor = 1.0

# Finite State Machine
class AresLidarParsingStatus:
    BEGIN = 0
    INFO = 1
    DISTANCE_MES = 2

class AresLidar:
    def __init__(self):
        self.parsing_status = AresLidarParsingStatus.BEGIN
        self.active_sensor = 0
        self.ROI_number = 0
        self.measure_number = 0
        self.rx_storage = bytearray(LIDAR_FRAME_SIZE * 2)
        self.measure = [[0, 0] for _ in range(LIDAR_MODULE_NUMBER)]

# Function to retrieve LidarDistance data
def get_lidar_data(lidar):
    reading_head = 0
    wait_for_head_cmp = 0
    wait_for_fill = 0

    while reading_head < len(lidar.rx_storage):
        reading_head_limit = len(lidar.rx_storage) if reading_head < LIDAR_FRAME_SIZE else LIDAR_FRAME_SIZE

        while reading_head < reading_head_limit:
            if lidar.parsing_status == AresLidarParsingStatus.BEGIN:
                if lidar.rx_storage[reading_head] == 0xFF:
                    wait_for_head_cmp += 1
                else:
                    wait_for_head_cmp = 0

                if wait_for_head_cmp > 5:
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.INFO

            elif lidar.parsing_status == AresLidarParsingStatus.INFO:
                if wait_for_head_cmp == 0:
                    lidar.active_sensor = lidar.rx_storage[reading_head]
                    wait_for_head_cmp += 1
                elif wait_for_head_cmp == 1:
                    lidar.ROI_number = lidar.rx_storage[reading_head]
                    wait_for_head_cmp += 1
                elif wait_for_head_cmp > 1:
                    lidar.measure_number = lidar.rx_storage[reading_head]
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.DISTANCE_MES

            elif lidar.parsing_status == AresLidarParsingStatus.DISTANCE_MES:
                if wait_for_fill % 3 == 0 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][0] = lidar.rx_storage[reading_head]
                    wait_for_fill += 1
                elif wait_for_fill % 3 == 1 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][1] = lidar.rx_storage[reading_head]
                    lidar.measure[wait_for_head_cmp][1] <<= 8
                    wait_for_fill += 1
                elif wait_for_fill % 3 == 2 and wait_for_head_cmp < lidar.measure_number:
                    lidar.measure[wait_for_head_cmp][1] += lidar.rx_storage[reading_head]
                    wait_for_fill += 1
                    wait_for_head_cmp += 1

                if wait_for_head_cmp >= lidar.measure_number:
                    wait_for_fill = 0
                    wait_for_head_cmp = 0
                    lidar.parsing_status = AresLidarParsingStatus.BEGIN

            reading_head += 1
        if reading_head >= LIDAR_FRAME_SIZE:
            reading_head_limit = LIDAR_FRAME_SIZE

    return lidar

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
    speed_factor = 1.0
    step = distance / (2 * np.pi * WHEEL_RADIUS)
    stepper_left.setTargetPosition(step)
    stepper_right.setTargetPosition(-step)
    while abs(distance / 260 - stepper_left.getPosition()) >= 1e-2:
        lidar_data.rx_storage = ser.read(LIDAR_FRAME_SIZE * 2)
        processed_data = get_lidar_data(lidar_data)
        distances = [distance[1] for distance in processed_data.measure]
        min_distance = min(distances)
        if 1 <= min_distance <= 370:
            speed_factor = 0.0
        elif min_distance >= 370:
            speed_factor = 1.0
        stepper_left.setVelocityLimit(speed * speed_factor)
        stepper_right.setVelocityLimit(speed * speed_factor)
        time.sleep(0.001)
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


def find_screen_port():
    stlink_ports = [port.device for port in serial.tools.list_ports.comports() if "ST-Link" in port.description]
    if stlink_ports:
        return stlink_ports[0]
    else:
        return None

port = find_screen_port() 
baudrate = 115200  
timeout = 1
start_pin = 26

if port:
    ser = serial.Serial(port, baudrate, timeout=timeout)
else: 
    print("No screen device found on target !")
    exit()

while True:
    received_data = ser.readline().decode().strip()
    if len(received_data) != 0:
        strategy = int(received_data)
        break

ser.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(start_pin, GPIO.IN)
previous_state = GPIO.input(start_pin)

while True:
    current_state = GPIO.input(start_pin)
    
    if current_state != previous_state:
        print(strategy)
        break
    
    time.sleep(0.1)

stepper_left = stepper_init(723793, 5)
stepper_right = stepper_init(723793, 0)

ser = serial.Serial("/dev/ttyAMA1", baudrate=115200, timeout=5.0)
lidar_data = AresLidar()

if strategy == 0:
    pass
elif strategy == 1:
    pass
elif strategy == 2:
    pass
elif strategy == 3:
    pass
elif strategy == 4:
    pass
elif strategy == 5:
    move_forward(stepper_left, stepper_right, 1200)
    time.sleep(1)
    speed = 2
    rotate_left(stepper_left, stepper_right, 90)
    time.sleep(0.5)
    speed = 1
    move_forward(stepper_left, stepper_right, -600)
    time.sleep(1)
    speed = 2
    move_forward(stepper_left, stepper_right, 600)
    time.sleep(1)
    rotate_left(stepper_left, stepper_right, -270)
    time.sleep(0.5)
    speed = 1
    move_forward(stepper_left, stepper_right, 1200)





stepper_left.close()
stepper_right.close()
GPIO.cleanup()
