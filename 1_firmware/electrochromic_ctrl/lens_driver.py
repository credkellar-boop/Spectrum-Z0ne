# 1_firmware/electrochromic_ctrl/lens_driver.py

class ElectrochromicController:
    def __init__(self, pin_num=18):
        self.pin_num = pin_num
        self.current_tint = 0
        self.is_toggled = False
        self._setup_gpio()

    def _setup_gpio(self):
        pass

    def set_tint(self, level):
        self.current_tint = max(0, min(100, level))
        self._apply_pwm(self.current_tint)

    def toggle_sun_shade(self):
        if self.is_toggled:
            self.set_tint(0)
            self.is_toggled = False
        else:
            self.set_tint(90)
            self.is_toggled = True

    def _apply_pwm(self, duty_cycle):
        pass
