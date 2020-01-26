from cmd import Cmd
import include.strings as strings
from include.device import Device
import testCommand

class rUI(Cmd):
	prompt = "rUI> "
	intro = strings.banner	

	device = Device()
	testQueue = []

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

			if selection is "q":
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

	def do_test(self, inp):
		try:
			inp = inp.split()
			getattr(testCommand, 'do_'+inp[0])(self," ".join(inp[1:]))
		except AttributeError:
			print("Please enter a valid command")
		
	# [add, list, remove]
	def complete_test(self, text, line, begidx, endidx):
		testCommands = [command[3:] for command in dir(testCommand) if len(command) > 3 and command[:3] == "do_"]
		if text:
			return [ command for command in testCommands if command.startswith(text) ]
		else:
			return testCommands

	def do_runScript(self, inp):
		"Run a list of commands from a text file"

		print(type(inp))
		
# Driver 
p = rUI()
p.cmdloop()

