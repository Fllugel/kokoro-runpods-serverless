# Kokoro Serverless

<div align="center">

![Kokoro Serverless](https://img.shields.io/badge/Kokoro-Serverless-blue?style=for-the-badge&logo=python)
![RunPod](https://img.shields.io/badge/RunPod-Serverless-purple?style=for-the-badge&logo=runpod)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)

**High-Quality Text-to-Speech with Voice Mixing & Phonemes**

[Features](#features) • [API Usage](#api-usage) • [Deployment](#deployment) • [Clients](#clients)

</div>

---

## � Overview

**Kokoro Serverless** is a production-ready, serverless deployment of the Kokoro TTS model, optimized for RunPod. It provides an OpenAI-compatible API for high-quality text-to-speech generation, featuring advanced capabilities like voice mixing, word-level timestamps, and phoneme generation.

Built on top of `ghcr.io/remsky/kokoro-fastapi-gpu`, this serverless wrapper ensures **zero cold-start latency** for model loading (via volume caching) and **100% API compatibility** with the original project.

## ✨ Features

- �️ **High-Quality TTS**: Generate natural-sounding speech in multiple languages.
- 🎛️ **Voice Mixing**: Combine multiple voices (e.g., `af_bella+af_sky`) for unique outputs.
- ⏱️ **Word Timestamps**: Get precise start/end times for every word (SRT generation).
- 🔡 **Phonemization**: Convert text to phonemes for linguistic analysis.
- ⚡ **Serverless Optimized**:
  - **Fast Cold Starts**: Models cached to network volume.
  - **Auto-Scaling**: Scales to zero when idle, up to N workers under load.
  - **Cost-Efficient**: Pay only for the inference time you use.

## 🚀 Deployment

### One-Click Deploy (RunPod)

1. **Clone this repository**.
2. **Create a Network Volume** in RunPod (recommended 20GB) to cache models.
3. **Create a Serverless Endpoint**:
   - **Template**: Select this repository (or build your own template).
   - **Container Image**: `ghcr.io/arkodeepsen/kokoro-fastapi-serverless:latest`
   - **Environment Variables**:
     - `HF_HOME`: `/runpod-volume`
     - `TRANSFORMERS_CACHE`: `/runpod-volume`
   - **GPU**: NVIDIA RTX 3090 / 4090 / A4000 or better recommended.

## 📡 API Usage

The endpoint exposes a single entry point `/runsync` (or `/run` for async) that accepts a JSON payload. All original Kokoro endpoints are supported by wrapping them in an `input` object.

### 1. Standard Text-to-Speech
**Endpoint**: `/runsync`

```json
{
  "input": {
    "model": "kokoro",
    "input": "Hello world! This is Kokoro running on serverless.",
    "voice": "af_bella",
    "response_format": "mp3",
    "speed": 1.0
  }
}
```

### 2. Voice Combination
Mix two voices together by joining their IDs with `+`.

```json
{
  "input": {
    "model": "kokoro",
    "input": "This is a mixed voice.",
    "voice": "af_bella+af_sky",
    "response_format": "mp3"
  }
}
```

### 3. Captioned Speech (Timestamps)
Generate audio along with word-level timestamps (perfect for subtitles).

```json
{
  "input": {
    "endpoint": "/dev/captioned_speech",
    "method": "POST",
    "input": "Generate subtitles for this text.",
    "voice": "af_bella",
    "return_timestamps": true
  }
}
```

**Response:**
```json
{
  "audio": "base64_encoded_audio...",
  "timestamps": [
    {"word": "Generate", "start": 0.0, "end": 0.5},
    {"word": "subtitles", "start": 0.5, "end": 1.2},
    ...
  ]
}
```

### 4. Text to Phonemes
Convert text into its phonemic representation.

```json
{
  "input": {
    "endpoint": "/dev/phonemize",
    "method": "POST",
    "text": "Hello world",
    "language": "a"
  }
}
```

## � Clients

This repository includes two ready-to-use clients to interact with your endpoint.

### Streamlit Web App (`app.py`)
A full-featured GUI for generating audio, mixing voices, and creating SRT subtitles.

```bash
pip install -r requirements.txt
streamlit run app.py
```

### CLI Tool (`inference.py`)
A simple command-line tool for quick generations.

```bash
python inference.py --text "Hello there" --voice af_bella --output hello.mp3
```

## ⚙️ Configuration

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `HF_HOME` | Path to HuggingFace cache (use network volume) | `/runpod-volume` |
| `TRANSFORMERS_CACHE`| Path to Transformers cache | `/runpod-volume` |
| `PYTHONUNBUFFERED` | Set to `1` for real-time logging | `1` |

## 📜 License

This project is licensed under the Apache 2.0 License.