from functools import wraps

# Require Device function decorator. Use this on any method that requires a device to be set
def require_device(func):
    @wraps(func)
    def wrapper(self=None, *arg, **kwargs):
        # Only run the decorated function if serial is open
        if self.device.ser.is_open:
            func(self, *arg, **kwargs)
        else:
            print("No device! Please connect to a device with \"connectDevice\"")
    return wrapper
