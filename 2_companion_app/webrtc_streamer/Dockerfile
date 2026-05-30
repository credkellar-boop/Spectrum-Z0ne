FROM python:3.11-slim

WORKDIR /app

# Install native OS dependencies required for video decoding and hardware acceleration
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Cache dependency layer separately to boost development iteration speeds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stream_manager.py .

ENV PYTHONUNBUFFERED=1

# Expose WebRTC standard UDP port limits for signaling and network transmission
EXPOSE 8080 50000-50050/udp

CMD ["python", "stream_manager.py"]
