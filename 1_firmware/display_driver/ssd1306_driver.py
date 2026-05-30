import time
import smbus

# SSD1306 Commands
SSD1306_I2C_ADDR = 0x3C
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D

class SSD1306Driver:
    def __init__(self, width=128, height=64, i2c_bus=1, i2c_addr=SSD1306_I2C_ADDR):
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.i2c_addr = i2c_addr
        self.bus = smbus.SMBus(i2c_bus)
        self.buffer = [0] * (self.width * self.pages)
        self._initialize_display()

    def _command(self, cmd):
        self.bus.write_byte_data(self.i2c_addr, 0x00, cmd)

    def _data(self, data):
        self.bus.write_i2c_block_data(self.i2c_addr, 0x40, data)

    def _initialize_display(self):
        init_cmds = [
            SSD1306_DISPLAYOFF,
            SSD1306_SETDISPLAYCLOCKDIV, 0x80,
            SSD1306_SETMULTIPLEX, self.height - 1,
            SSD1306_SETDISPLAYOFFSET, 0x00,
            SSD1306_SETSTARTLINE | 0x00,
            SSD1306_CHARGEPUMP, 0x14,
            SSD1306_MEMORYMODE, 0x00,
            SSD1306_SEGREMAP | 0x01,
            SSD1306_COMSCANDEC,
            SSD1306_SETCOMPINS, 0x12 if self.height == 64 else 0x02,
            SSD1306_SETCONTRAST, 0xCF,
            SSD1306_SETPRECHARGE, 0xF1,
            SSD1306_SETVCOMDETECT, 0x40,
            SSD1306_DISPLAYALLON_RESUME,
            SSD1306_NORMALDISPLAY,
            SSD1306_DISPLAYON
        ]
        for cmd in init_cmds:
            self._command(cmd)
        self.clear()
        self.update()

    def clear(self):
        self.buffer = [0] * (self.width * self.pages)

    def draw_pixel(self, x, y, color=1):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        page = y // 8
        bit_mask = 1 << (y % 8)
        if color:
            self.buffer[x + (page * self.width)] |= bit_mask
        else:
            self.buffer[x + (page * self.width)] &= ~bit_mask

    def draw_text(self, text, x, y):
        for i, char in enumerate(text):
            char_x = x + (i * 6)
            if char_x >= self.width:
                break
            for dx in range(5):
                for dy in range(7):
                    self.draw_pixel(char_x + dx, y + dy, 1)

    def update(self):
        self._command(SSD1306_COLUMNADDR)
        self._command(0)
        self._command(self.width - 1)
        self._command(SSD1306_PAGEADDR)
        self._command(0)
        self._command(self.pages - 1)

        for i in range(0, len(self.buffer), 16):
            self._data(self.buffer[i:i+16])
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
