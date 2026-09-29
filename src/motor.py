import time
import RPi.GPIO as GPIO

class MotorTrigger:
    def __init__(self, pin, duration_sec=5, cooldown_sec=30):
        self.pin = pin
        self.duration = duration_sec
        self.cooldown = cooldown_sec
        self.last_trigger = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def trigger(self, class_name, allowed_classes):
        if class_name not in allowed_classes:
            return False
        now = time.time()
        if now - self.last_trigger < self.cooldown:
            return False
        print(f'[MOTOR] Triggering for {class_name}')
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(self.duration)
        GPIO.output(self.pin, GPIO.LOW)
        self.last_trigger = now
        return True

    def cleanup(self):
        GPIO.cleanup()
