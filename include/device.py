import serial
from serial.tools import list_ports
import select

class Device():
	# Define device parameters
	baudrate = 115200
	port = None
	timeout = 5	
	ser = None

	def __init__(self):
		self.ser = serial.Serial()
		self.ser.baudrate = self.baudrate
		self.ser.timeout = self.timeout

	def setPort(self, portName):
		self.ser.port = portName

	def openPort(self):
		self.ser.open()
		return self.ser.is_open

	def isOpen(self):
		return self.ser.is_open

	def readLine(self):
		return self.ser.readlines()

	def requestData(self, command, length=1, stopbyte=b""):
		# Make sure we are connected to the device
		if not self.isOpen():
			print("Device not connected")
			return False
		# Ask the device for a response
		self.ser.write(command)
		# Compose the response, ending it when it equals a terminator byte, is out of data, or hits a specified length
		response = b""
		lastbyte = None
		while lastbyte != stopbyte and lastbyte != b"" and len(response) < length:
			lastbyte = self.ser.read()
			response += lastbyte
		return response

	def listDevices(self):
		return list_ports.comports()
