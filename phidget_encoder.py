from Phidget22.Phidget import *
from Phidget22.Devices.Encoder import *
import time

def onPositionChange(self, positionChange, timeChange, indexTriggered):
	# print("PositionChange: " + str(positionChange))
	# print("TimeChange: " + str(timeChange))
	# print("IndexTriggered: " + str(indexTriggered))
	print("getPosition: " + str(self.getPosition()))
	print("----------")

def main():
	encoder1 = Encoder()
	encoder0 = Encoder()

	encoder1.setHubPort(4)
	encoder0.setHubPort(1)
	encoder0.setDeviceSerialNumber(723793)
	encoder1.setDeviceSerialNumber(723793)

	encoder0.setOnPositionChangeHandler(onPositionChange)
	encoder1.setOnPositionChangeHandler(onPositionChange)

	encoder0.openWaitForAttachment(5000)
	encoder1.openWaitForAttachment(5000)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	encoder0.close()
	encoder1.close()

main()
