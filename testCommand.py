def do_addTest(self, inp):
	"Add a test to the queue"
	#####
	# CREATE TEST OBJECT HERE
	# assign it to testObject variable
	#
	#####
	testObject = inp
	self.testQueue.append(testObject)
	print("Added", testObject, "to queue.")

def do_listTestQueue(self, inp):
	"List the currently queued tests"

	if not self.testQueue:
		print("The test queue is empty")
		return
	for i, testObject in enumerate(self.testQueue):
		print("["+str(i)+"] "+testObject)

def do_removeTest(self, inp):
	"""Remove a test
		-- input is test number from `listTests`
		-- use `remove -f <testNumber> to skip confirmation"""
	inp = inp.split()
	if len(inp) < 1:
		print("Please input a test number")
		return
	try:
		if inp[0] != '-f':
			toRemoveIndex = int(inp[0])
			ans = input("Are you sure you would like to remove "+str(self.testQueue[toRemoveIndex])+" from the testQueue? Y/n")
			if not (ans.lower() == "y" or ans.lower() == "yes" or ans.lower() == ""):
				print("Canceling...")
				return
		else:
			toRemoveIndex = int(inp[1])
		print("Removed", self.testQueue.pop(toRemoveIndex),"from queue.")
	except ValueError:
		print("Please input a valid test number")