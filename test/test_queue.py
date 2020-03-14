import unittest
from unittest.mock import patch
from io import StringIO
import include.testCommand as testCommand
from rUI import rUI, Device
from tests.DummyTest1 import DummyTest1
import serial

class Test_Queue(unittest.TestCase):
    """Tests queue class by loading a test YAML file and managing its tests"""
    def setUp(self):
        self.rUI = rUI()
        # Since these are class variables, they need to be reset between tests
        self.rUI.device = Device()
        # Override the serial object with a loopback device
        self.rUI.device.ser = serial.serial_for_url("loop://")
        self.rUI.testQueue = []

    def test_add(self):
        """Adds one file to the queue and checks the queue to ensure it is consistent"""
        testCommand.do_add(self.rUI, "testPlan.yaml")
        self.assertEqual(len(self.rUI.testQueue), 2)
        self.assertIsInstance(self.rUI.testQueue[0], DummyTest1)
        self.assertIsInstance(self.rUI.testQueue[1], DummyTest1)

    def test_remove(self):
        """Adds one file to the queue, removes it, and makes sure the queue is empty"""
        testCommand.do_add(self.rUI, "testPlan.yaml")
        testCommand.do_remove(self.rUI, "-f 1")
        testCommand.do_remove(self.rUI, "-f 0")
        self.assertEqual(len(self.rUI.testQueue), 0)

    def test_run(self):
        """Runs a full test plan and makes sure there are no remaining tests once done"""
        testCommand.do_add(self.rUI, "testPlan.yaml")
        testCommand.do_run(self.rUI, "0")
        self.assertEqual(len(self.rUI.testQueue), 1)
        testCommand.do_run(self.rUI, None)
        self.assertEqual(len(self.rUI.testQueue), 0)

    def test_list(self):
        """Adds three objects to the test queue and checks to make sure they are listed in order"""
        testCommand.do_add(self.rUI, "testPlan.yaml")
        # Capture output from the console and redirect it to a variable
        with patch('sys.stdout', new=StringIO()) as output:
            testCommand.do_list(self.rUI, None)
            self.assertEqual(output.getvalue().strip(), "[0] dummytest1 -- duration: 0\n[1] dummytest1 -- duration: 1")


