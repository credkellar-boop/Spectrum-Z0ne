from machine import Pin, PWM
import time

class ElectrochromicController:
    def __init__(self, pin_num: int, frequency: int = 500):
        """Initializes the lens driver using a hardware PWM pin."""
        # Setup the GPIO pin for Pulse Width Modulation
        self.pwm_pin = PWM(Pin(pin_num))
        self.pwm_pin.freq(frequency)
        self.current_tint = 0  # Percentage (0% to 100%)
        self.set_tint(0)       # Start fully transparent

    def set_tint(self, percentage: int):
        """
        Adjusts the voltage to the lens to change tint levels.
        percentage: 0 (Clear) to 100 (Deep Sun Shade Mode)
        """
        if not (0 <= percentage <= 100):
            raise ValueError("Tint percentage must be between 0 and 100")
            
        # MicroPython PWM duty cycle spans from 0 to 1023
        duty_cycle = int((percentage / 100) * 1023)
        self.pwm_pin.duty(duty_cycle)
        self.current_tint = percentage
        print(f"[FIRMWARE] Lens opacity updated to: {self.current_tint}%")

    def toggle_sun_shade(self):
        """Quick toggle shortcut for voice/gesture activation."""
        if self.current_tint > 20:
            self.set_tint(0)   # Clear mode
        else:
            self.set_tint(90)  # Max sun shade mode

    def deinit(self):
        """Safely powers down the lens layer to prevent burn-in."""
        self.pwm_pin.deinit()
