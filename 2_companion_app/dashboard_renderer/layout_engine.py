import json
import time

class VisualHubRenderer:
    def __init__(self, display_width=1280, display_height=720):
        """Initializes the virtual canvas coordinate matrix for the HUD."""
        self.width = display_width
        self.height = display_height
        self.ui_state = {
            "streaming": False,
            "sun_shade_level": 0,
            "crypto_ticker": "BTC: --",
            "gemini_text": "",
            "detected_faces": []
        }

    def update_state(self, key: str, value):
        """Updates a specific metric in the dashboard state machine."""
        if key in self.ui_state:
            self.ui_state[key] = value

    def compile_hud_commands(self) -> str:
        """
        Translates raw app state into a compact stream of layout commands
        optimized for the micro-OLED display driver to interpret.
        """
        commands = []

        # 1. Top Bar: Status indicators (Streaming and Sun Shade mode)
        stream_status = "🔴 LIVE" if self.ui_state["streaming"] else "⚪ IDLE"
        commands.append({
            "type": "TEXT", "x": 40, "y": 40, 
            "content": f"REC: {stream_status} | SHADE: {self.ui_state['sun_shade_level']}%", 
            "color": "0xFF0000" if self.ui_state["streaming"] else "0xFFFFFF"
        })

        # 2. Top Right: Real-time Cryptocurrency Alert Feed
        commands.append({
            "type": "TEXT", "x": self.width - 250, "y": 40, 
            "content": self.ui_state["crypto_ticker"], 
            "color": "0x00FF00"
        })

        # 3. Center Screen: Spatial Face Recognition Bounding Boxes
        for face in self.ui_state["detected_faces"]:
            # Coordinate tracking matches the 4K camera viewport to display space
            commands.append({
                "type": "RECT", 
                "x": face["x"], "y": face["y"], 
                "w": face["w"], "h": face["h"], 
                "color": "0x00FFFF" # Cyan target box
            })
            commands.append({
                "type": "TEXT", "x": face["x"], "y": face["y"] - 20, 
                "content": face["name"], "color": "0x00FFFF"
            })

        # 4. Bottom Center: Subtitles / Gemini Conversation Output
        if self.ui_state["gemini_text"]:
            commands.append({
                "type": "TEXT", "x": self.width // 4, "y": self.height - 80, 
                "content": self.ui_state["gemini_text"], 
                "color": "0xFFFF00" # Yellow for high visibility readability
            })

        # Pack the drawing pipeline into a minimal JSON payload
        return json.dumps({"timestamp": time.time(), "pipeline": commands})

# Quick verification block
if __name__ == "__main__":
    hub = VisualHubRenderer()
    hub.update_state("crypto_ticker", "MONAD: $4.20 (+12%)")
    hub.update_state("detected_faces", [{"x": 500, "y": 200, "w": 150, "h": 150, "name": "Dev Partner"}])
    hub.update_state("gemini_text", "Gemini: Smart Tinting Active.")
    
    # This JSON string is what gets shot across the local network to the glasses
    print(hub.compile_hud_commands())
