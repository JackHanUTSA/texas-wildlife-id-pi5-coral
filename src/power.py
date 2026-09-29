import time

class PowerManager:
    def __init__(self, threshold=20, pin=None):
        self.threshold = threshold
        self.pin = pin
        self.battery_level = 100

    def read_battery(self):
        return self.battery_level

    def check(self):
        level = self.read_battery()
        if level < self.threshold:
            print(f'[POWER] Low battery {level}%')
            return False
        return True
