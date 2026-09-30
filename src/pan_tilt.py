import RPi.GPIO as GPIO
import time

class PanTilt:
    def __init__(self, pan_pin, tilt_pin):
        GPIO.setmode(GPIO.BCM)
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        GPIO.setup(self.pan_pin, GPIO.OUT)
        GPIO.setup(self.tilt_pin, GPIO.OUT)
        self.pan_pwm = GPIO.PWM(self.pan_pin, 50)
        self.tilt_pwm = GPIO.PWM(self.tilt_pin, 50)
        self.pan_pwm.start(0)
        self.tilt_pwm.start(0)
        self.current_pan = 90
        self.current_tilt = 90

    def angle_to_duty(self, angle):
        duty = 2.5 + (angle / 180.0) * 10.0
        return duty

    def set_pan(self, angle):
        angle = max(0, min(180, angle))
        duty = self.angle_to_duty(angle)
        self.pan_pwm.ChangeDutyCycle(duty)
        self.current_pan = angle
        time.sleep(0.3)

    def set_tilt(self, angle):
        angle = max(0, min(180, angle))
        duty = self.angle_to_duty(angle)
        self.tilt_pwm.ChangeDutyCycle(duty)
        self.current_tilt = angle
        time.sleep(0.3)

    def sweep(self, pan_min, pan_max, tilt_min, tilt_max):
        for pan in range(pan_min, pan_max+1, 5):
            self.set_pan(pan)
        for pan in range(pan_max, pan_min-1, -5):
            self.set_pan(pan)

    def stop(self):
        self.pan_pwm.stop()
        self.tilt_pwm.stop()
        GPIO.cleanup([self.pan_pin, self.tilt_pin])
