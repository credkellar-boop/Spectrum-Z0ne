import machine
import ssd1306  # Standard MicroPython OLED library
import json

class SpectrumDisplayDriver:
    def __init__(self, spi_bus_id=1, sck_pin=14, mosi_pin=13, dc_pin=4, res_pin=5, cs_pin=15):
        """Initializes the physical SPI interface to the Micro-OLED lenses."""
        self.width = 1280  # Virtualized coordinate mapping
        self.height = 720
        
        # Setup hardware SPI pins
        self.spi = machine.SPI(spi_bus_id, baudrate=8000000, polarity=0, phase=0, 
                               sck=machine.Pin(sck_pin), mosi=machine.Pin(mosi_pin))
        
        # Control pins for the display panel
        self.dc = machine.Pin(dc_pin, machine.Pin.OUT)
        self.res = machine.Pin(res_pin, machine.Pin.OUT)
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)
        
        # Physical micro-display panel driver instance (scaled down or mirrored)
        # For prototyping, we map down to the display hardware size (e.g., 128x64 or custom resolution)
        self.oled = ssd1306.SSD1306_SPI(128, 64, self.spi, self.dc, self.res, self.cs)
        self.clear_display()

    def clear_display(self):
        self.oled.fill(0)
        self.oled.show()

    def scale_coordinate(self, x, y):
        """Maps companion app 1280x720 UI space down to physical micro-display matrix."""
        scaled_x = int((x / self.width) * 128)
        scaled_y = int((y / self.height) * 64)
        return scaled_x, scaled_y

    def execute_render_pipeline(self, json_payload: str):
        """Parses drawing primitives from the companion app and updates the glass lens matrix."""
        try:
            data = json.loads(json_payload)
            self.oled.fill(0)  # Clear back-buffer to prevent frame ghosting
            
            for cmd in data.get("pipeline", []):
                if cmd["type"] == "TEXT":
                    x, y = self.scale_coordinate(cmd["x"], cmd["y"])
                    # MicroPython natively draws text via built-in framebuffer fonts
                    self.oled.text(cmd["content"], x, y, 1)
                    
                elif cmd["type"] == "RECT":
                    x, y = self.scale_coordinate(cmd["x"], cmd["y"])
                    w, h = int((cmd["w"] / self.width) * 128), int((cmd["h"] / self.height) * 64)
                    self.oled.rect(x, y, w, h, 1)
            
            # Flush the back-buffer instantly to the waveguides
            self.oled.show()
            
        except Exception as e:
            print(f"[FIRMWARE ERROR] Frame draw dropped: {e}")

# Simulate frame reception loop over serial/BLE bus
def start_firmware_receiver():
    display = SpectrumDisplayDriver()
    print("[FIRMWARE] Waveguide Render Pipeline Listening...")
    
    import sys
    while True:
        # Check if a command package string has dropped into the hardware bus channel
        line = sys.stdin.readline().strip()
        if line.startswith('{"timestamp"'):
            display.execute_render_pipeline(line)

if __name__ == "__main__":
    start_firmware_receiver()
