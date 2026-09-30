import RPi.GPIO as GPIO
import time

class FanController:
    def __init__(self, pin, pwm_freq=25000, min_duty=30, max_duty=100):
        self.pin = pin
        self.min_duty = min_duty
        self.max_duty = max_duty
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, pwm_freq)
        self.pwm.start(0)
        self.current_duty = 0

    def set_duty(self, duty):
        duty = max(0, min(self.max_duty, duty))
        self.pwm.ChangeDutyCycle(duty)
        self.current_duty = duty

    def control_by_temp(self, temp, threshold=55):
        if temp is None:
            return
        if temp < threshold - 10:
            self.set_duty(0)
        elif temp < threshold:
            ratio = (temp - (threshold - 10)) / 10.0
            duty = self.min_duty + ratio * (self.max_duty - self.min_duty)
            self.set_duty(duty)
        else:
            self.set_duty(self.max_duty)

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup(self.pin)
