import time

try:
    import board
    import adafruit_bme280.advanced as adafruit_bme280
    BME_AVAILABLE = True
except Exception:
    BME_AVAILABLE = False

class ClimateSensor:
    def __init__(self, sensor_type='bme280', i2c_bus=1, address=0x76):
        self.sensor_type = sensor_type
        self.enabled = BME_AVAILABLE
        if self.enabled and sensor_type == 'bme280':
            i2c = board.I2C()
            self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=address)
        else:
            self.sensor = None

    def read(self):
        if not self.enabled or self.sensor is None:
            return {'temperature': 25.0, 'humidity': 50.0, 'pressure': 1013.25}
        try:
            temp = self.sensor.temperature
            humidity = self.sensor.humidity
            pressure = self.sensor.pressure
            return {'temperature': temp, 'humidity': humidity, 'pressure': pressure}
        except Exception:
            return {'temperature': None, 'humidity': None, 'pressure': None}
