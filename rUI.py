from cmd import Cmd
import include.strings as strings
from include.device import Device

class rUI(Cmd):
	prompt = "rUI> "
	intro = strings.banner	

	device = Device()

	def do_exit(self, inp):
		"Exit the rUI"
		print(strings.outro)
		return True

	def do_connectDevice(self, inp):
		"Connect to a serial device"
		# Get a list of the available serial ports
		ports = self.device.listDevices() 
		portNames = []
	
		# Get device names and print to screen
		i = 0
		for port in ports:
			portNames.append(port.device)
			# Format
			print(str(i) + "     " + str(port))
			i = i + 1
		
		# Prompt user to select serial device
		while True:
			selection = input("Enter selection[q(quit)]: ")

			if selection == "q":
				return False
			
			# Verify valid selction	
			try:
				selection = int(selection)
			except:
				print("Invalid option...try again")
				continue
			
			if selection < len(portNames):
				self.device.setPort(portNames[selection])
				self.device.openPort()
				break
			else:
				print("Selection out of range...try again")

	def do_listen(self, inp):
		"Read from device"
		# Ensure serial port is open 
		print("Enter CTRL-c to terminate read")
		try:
			while True:
				if True:
					print(str(self.device.readLine(), 'utf-8'))
		except KeyboardInterrupt:
			print("Read terminated")

	def do_getStatus(self, inp):
		"Gets status of the peripheral device"
		# Make sure we are connected to the device
		response = self.device.requestData([1])
		if response == b"\x01":
			print("Peripheral is OK")
		elif len(response) > 0:
			print("Peripheral is in error state {state}").format(state=ord(response))
		else:
			print("Error: no response from device")


# Driver 
p = rUI()
p.cmdloop()

