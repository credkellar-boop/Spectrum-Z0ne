import sys
import select
from lens_driver import ElectrochromicController

def listen_for_commands():
    # Initialize lens hardware on GPIO pin 18
    lens = ElectrochromicController(pin_num=18)
    print("[FIRMWARE] Spectrum-Z0ne Hardware Layer Online.")

    while True:
        # Check for incoming commands over UART/Serial
        if select.select([sys.stdin], [], [], 0.1)[0]:
            command = sys.stdin.readline().strip()

            if command == "SHADE_ON":
                lens.set_tint(90)
            elif command == "SHADE_OFF":
                lens.set_tint(0)
            elif command == "SHADE_TOGGLE":
                lens.toggle_sun_shade()
            elif command.startswith("SHADE_SET:"):
                try:
                    val = int(command.split(":")[1])
                    lens.set_tint(val)
                except ValueError:
                    print("[ERROR] Invalid tint format.")

if __name__ == "__main__":
    listen_for_commands()
