# 1_firmware/ipc_bridge.py
import subprocess
import os

class IPCBridge:
    def __init__(self, firmware_path="electrochromic_ctrl/main.py"):
        self.process = subprocess.Popen(
            ['python3', firmware_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

    def send_command(self, cmd):
        if self.process.poll() is None:
            self.process.stdin.write(f"{cmd}\n")
            self.process.stdin.flush()
            print(f"[IPC] Sent: {cmd}")

    def stop(self):
        self.process.terminate()

# Example Usage:
if __name__ == "__main__":
    bridge = IPCBridge()
    # Now your Gemini agent can trigger hardware events
    bridge.send_command("SHADE_SET:50")
