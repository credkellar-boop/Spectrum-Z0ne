# Spectrum-Z0ne 🕶️

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![CI Build](https://img.shields.io/badge/CI%20Build-passing-brightgreen.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Firmware](https://img.shields.io/badge/firmware-MicroPython-red.svg)
![AI](https://img.shields.io/badge/AI-Gemini%203.5%20Flash-orange.svg)
[![Crates.io](https://img.shields.io/crates/v/spectrum-z0ne.svg)](https://crates.io/crates/spectrum-z0ne)

Spectrum-Z0ne is a next-generation, production-ready augmented reality (AR) wearable ecosystem designed to redefine spatial computing. Featuring adaptive electrochromic sun shading, it projects a brilliant Visual Hub dashboard via micro-OLED waveguides. 

By aggressively decoupling heavy computational processing from the head-worn device, Spectrum-Z0ne achieves high-performance multimodal AI features and low-latency rendering without the heavy thermal and weight footprints that plague traditional AR headsets.

## 🚀 Core Architecture

1. **The Wearable (Thin Client):** Runs in a bare-metal MicroPython environment on an ultra-low-power SoC (e.g., Qualcomm AR2 co-processor). It drives the electrochromic lenses via hardware Pulse Width Modulation (PWM), reads raw camera buffers, and prints vector primitives straight onto the Micro-OLED display registers.
2. **The Companion App Layer (Host Compute):** Runs on a local high-performance host (smartphone or compute puck). It intercepts raw camera data via Wi-Fi Direct, compresses it into hardware-accelerated H.265/AV1 streams for WebRTC broadcasting, evaluates localized machine learning loops, and compiles spatial UI updates into optimized JSON layouts.
3. **The Intelligent Cloud Bridge:** Connects asynchronous voice prompts and context-aware vision buffers to the Gemini Pro/Flash APIs for intent resolution.

## 📂 Project Structure

This monorepo isolates hardware constraints from application-level logic through explicit boundary directories:

```text
Spectrum-Z0ne/
├── .github/
│   └── workflows/
│       ├── ci.yml                      # CI pipeline for testing and validation
│       └── publish.yml                 # Automated crates.io deployment
├── 1_firmware/                         # Bare-metal wearable code
│   ├── display_driver/
│   │   └── ssd1306_driver.py           # Micro-OLED dashboard control
│   └── electrochromic_ctrl/
│       └── lens_driver.py              # Adaptive sun shading PWM control
├── 2_companion_app/                    # Host compute layer (Smartphone/Puck)
├── 3_ai_services/                      # Gemini 3.5 Flash integration & multimodal processing
├── 4_infrastructure/                   # Cloud relays, streaming relays, and backend
├── ai_service/                         # Local AI processing and intent resolution
├── src/                                # Core Rust implementation (spectrum-z0ne crate)
├── webrtc_streamer/                    # Low-latency H.265/AV1 camera streaming
├── .env                                # Environment configurations
├── .gitignore                          # Git ignore rules
├── Cargo.toml                          # Rust package manifest
└── README.md                           # Project documentation
