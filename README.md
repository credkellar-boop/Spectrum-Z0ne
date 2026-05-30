# Spectrum-Z0ne 🕶️

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![CI Build](https://img.shields.io/badge/CI%20Build-passing-brightgreen?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.11%2B-brightgreen?style=flat-square&logo=python)
![MicroPython](https://img.shields.io/badge/firmware-MicroPython-red?style=flat-square)
![API](https://img.shields.io/badge/AI-Gemini%203.5%20Flash-orange?style=flat-square&logo=google-gemini)


**Spectrum-Z0ne** is an advanced, production-ready augmented reality (AR) wearable ecosystem designed to redefine spatial computing. By decoupling heavy computational processing from the head-worn device, Spectrum-Z0ne achieves high-performance multimodal AI features and low-latency rendering without the heavy thermal and weight footprints traditional AR headsets face.

The ecosystem integrates adaptive electrochromic sun-shading, real-time spatial telemetry overlaying a high-brightness Micro-OLED Visual Hub, local face authentication, and ultra-low-latency 4K video live-streaming via a split-processing pipeline managed by a companion device and Google's Gemini network.

---

## 🛰️ Architecture & Split-Processing Pipeline

To keep the glasses structurally lightweight and thermoelectrically viable, Spectrum-Z0ne utilizes a **Tethered Co-Processing Topology**:

1. **The Edge Layer (Glasses Firmware):** Runs a bare-metal MicroPython/Zephyr RTOS environment on an ultra-low-power SoC (e.g., Qualcomm AR2 co-processor). It drives the electrochromic lenses via hardware Pulse Width Modulation (PWM), reads raw camera buffers, and prints vector primitives straight onto the Micro-OLED display registers.
2. **The Companion App Layer (Host Compute):** Runs on a local high-performance host (smartphone or compute puck). It intercepts raw camera data via Wi-Fi Direct, compresses it into hardware-accelerated H.265/AV1 streams for WebRTC broadcasting, evaluates localized machine learning loops, and compiles spatial UI updates into optimized JSON layouts.
3. **The Intelligent Cloud Bridge:** Connects asynchronous voice prompts and context-aware vision buffers to the Gemini Pro/Flash APIs for intent resolution.

---

## 📂 Project Structure

This monorepo isolates hardware constraints from application-level logic through explicit boundary directories:

```text
Spectrum-Z0ne/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions continuous integration pipeline
├── 1_firmware/                     # Bare-metal microcontroller code (Glasses)
│   ├── display_driver/
│   │   └── ssd1306_driver.py       # SPI register layout mapping JSON primitives to pixels
│   ├── electrochromic_ctrl/
│   │   ├── lens_driver.py          # Hardware-level PWM frequency/duty-cycle tint controller
│   │   └── main.py                 # Serial/UART peripheral listener loop
│   └── sensor_fusion/              # IMU telemetry and raw camera frame buffers
├── 2_companion_app/                # High-compute translation layer (Host Phone/Puck)
│   ├── ai_pipeline/                # Audio-to-text telemetry and token processing
│   ├── dashboard_renderer/
│   │   └── layout_engine.py        # Compiles UI coordinates into compact graphic arrays
│   └── webrtc_streamer/
│       └── stream_manager.py       # Real-time 4K image capturing and UDP network relays
├── 3_ai_services/                  # Neural network interfaces & bridges
│   ├── gemini_bridge/
│   │   ├── main.py                 # Async IO Client connection to Gemini API 
│   │   └── requirements.txt        # Python package manifests for the AI layer
│   ├── local_face_auth/            # Lightweight mobile edge face boundaries (ONNX/TFLite)
│   └── local_wake_word/            # Continuous low-power voice wake monitoring
└── 4_infrastructure/               # Distributed backend pipelines
    ├── device_management/          # Signed binary Over-The-Air (OTA) firmware deployment
    └── streaming_relay/            # High-throughput RTMP/WebRTC broadcast infrastructure

===================================================

# Clone the repository
git clone [https://github.com/credkellar-boop/Spectrum-Z0ne.git](https://github.com/credkellar-boop/Spectrum-Z0ne.git)
cd Spectrum-Z0ne

# Configure your environment matrix (Excluded from git tracking)
echo "GEMINI_API_KEY=your_secret_production_key" > .env

cd ../../2_companion_app/dashboard_renderer
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r ../../3_ai_services/gemini_bridge/requirements.txt
python layout_engine.py
