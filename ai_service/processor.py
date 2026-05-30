from ipc_bridge import IPCBridge
import time

class AIHardwareAutomator:
    def __init__(self):
        self.bridge = IPCBridge()
        
    def process_frame(self, light_intensity):
        """
        Light intensity is a value from 0-1000.
        If environment is too bright, shade it.
        """
        if light_intensity > 700:
            self.bridge.send_command("SHADE_SET:90")
            print("[AI] Brightness detected. Tinting lenses.")
        elif light_intensity < 200:
            self.bridge.send_command("SHADE_OFF")
            print("[AI] Low light detected. Clearing lenses.")

    def run_inference_loop(self):
        # Placeholder for your real-time camera/light sensor loop
        print("[AI] Monitoring environment...")
        try:
            while True:
                # Simulated light sensor reading
                current_light = 800 
                self.process_frame(current_light)
                time.sleep(5)
        except KeyboardInterrupt:
            self.bridge.stop()

if __name__ == "__main__":
    automator = AIHardwareAutomator()
    automator.run_inference_loop()
