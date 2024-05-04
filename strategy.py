import serial
import serial.tools.list_ports
import RPi.GPIO as GPIO
import time

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
        strategy = received_data
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

GPIO.cleanup()
