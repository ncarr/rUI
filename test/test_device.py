from include.device import Device
import unittest
import serial


class Test_Device(unittest.TestCase):
    """Tests Device class without requiring a connected hardware device"""
    def setUp(self):
        self.device = Device()

    def test_setPort(self):
        """Sets the port to COM8 and None and checks to make sure the port was set to the correct value"""
        port = 'COM8'
        self.device.setPort(port)
        self.assertEqual(self.device.ser.port, port)
        self.device.setPort(None)
        self.assertIsNone(self.device.ser.port)

    def test_openPort(self):
        """Opens a port, then checks to make sure it returns True and the port is marked as open"""
        # Replace the serial port with a loopback device that has not been opened yet
        self.device.ser = serial.serial_for_url('loop://', do_not_open=True)
        self.assertTrue(self.device.openPort())
        self.assertTrue(self.device.ser.is_open)

    def test_closePort(self):
        """Closes a port, then checks to make sure it returns False and the port is not marked as open"""
        self.device.ser = serial.serial_for_url('loop://')
        self.assertFalse(self.device.closePort())
        self.assertFalse(self.device.ser.is_open)

    def test_getPort(self):
        """Gets the current port, then checks to make sure the initial state is None, sets it to loop:// and checks to see if getPort now returns that value"""
        self.assertIsNone(self.device.getPort())
        # Set the port to loopback
        self.device.ser = serial.serial_for_url('loop://', do_not_open=True)
        self.assertEqual(self.device.getPort(), self.device.ser.port)
        self.assertEqual(self.device.getPort(), 'loop://')

    def test_isOpen(self):
        """Checks to see if isOpen matches the serial module's internal is_open value"""
        self.assertEqual(self.device.isOpen(), self.device.ser.is_open)

    def test_readLine(self):
        """Checks to see if readLine returns a list with one bytes element"""
        # Set the port to loopback
        self.device.ser = serial.serial_for_url('loop://')
        self.device.ser.timeout = 5
        self.device.ser.write(b'\x00\x00\x00\x00\x00\n')
        line = self.device.readLine()
        self.assertIsInstance(line, list)
        self.assertEqual(len(line), 1)
        self.assertIsInstance(line[0], bytes)

    def test_listDevices(self):
        """Checks to see if listDevices returns a list"""
        self.assertIsInstance(self.device.listDevices(), list)

    def test_readBytes(self):
        """Reads 5 bytes, then checks to make sure readBytes returns a bytes object of length 5"""
        length = 5
        # Set the port to loopback
        self.device.ser = serial.serial_for_url('loop://')
        self.device.ser.timeout = 5
        # Send test data
        self.device.ser.write(b'\x00\x00\x00\x00\x00')
        # Read test data
        data = self.device.readBytes(length)
        self.assertIsInstance(data, bytes)
        self.assertEqual(len(data), length)

    def test_writeBytes(self):
        # Set the port to loopback
        self.device.ser = serial.serial_for_url('loop://')
        self.device.ser.timeout = 5
        """Writes valid data to a file and then tries to write data that is too long"""
        self.assertNotEqual(self.device.writeBytes(
            b"Lorem ipsum dolor sit amet, consectetur adipiscing elit posuere."),
            False)
        # Boundary condition: equals MAXSIZE
        self.assertFalse(self.device.writeBytes(
            b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sollicitudin maximus dolor elementum interdum. Ut at nulla convallis odio feugiat iaculis in sit amet nibh. Aenean efficitur ut volutpat."))
        # Boundary condition: 1 over MAXSIZE
        self.assertFalse(self.device.writeBytes(
            b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi sollicitudin maximus dolor elementum interdum. Ut at nulla convallis odio feugiat iaculis in sit amet nibh. Aenean efficitur ut volutpat. "
        ))

    def test_writeInt8(self):
        """Writes 126 and checks to make sure it runs successfully"""
        # Set the port to loopback
        self.device.ser = serial.serial_for_url('loop://')
        self.device.ser.timeout = 5
        self.assertNotEqual(self.device.writeInt8(126), False)
