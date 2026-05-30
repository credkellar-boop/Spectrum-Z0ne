import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Fallback for local development/testing without physical hardware
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode): pass
        @staticmethod
        def setwarnings(flag): pass
        @staticmethod
        def cleanup(): pass
        class PWM:
            def __init__(self, pin, freq): pass
            def start(self, dc): pass
            def ChangeDutyCycle(self, dc): pass
            def stop(self): pass
        @staticmethod
        def PWM(pin, freq): return MockGPIO.PWM(pin, freq)
    GPIO = MockGPIO

class ElectrochromicController:
    def __init__(self, pin_num=18, pwm_frequency=1000):
        self.pin_num = pin_num
        self.pwm_frequency = pwm_frequency
        self.current_tint = 0
        self.is_toggled = False
        self.pwm = None
        self._setup_gpio()

    def _setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_num, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin_num, self.pwm_frequency)
        self.pwm.start(0)

    def set_tint(self, level):
        self.current_tint = max(0, min(100, level))
        self._apply_pwm(self.current_tint)
        self.is_toggled = self.current_tint >= 50

    def toggle_sun_shade(self):
        if self.is_toggled:
            self.set_tint(0)
            self.is_toggled = False
        else:
            self.set_tint(90)
            self.is_toggled = True

    def _apply_pwm(self, duty_cycle):
        if self.pwm:
            self.pwm.ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()
