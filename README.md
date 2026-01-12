# CAPTCHA+ 🖐️

A gesture-based authentication system that uses computer vision to verify you're human—no more clicking on traffic lights!

## What is this?

CAPTCHA+ is a creative reimagining of the traditional CAPTCHA system. Instead of selecting images or deciphering distorted text, users authenticate by showing hand gestures to their webcam. The system uses real-time hand tracking to recognize gestures and verify human presence.

## How it Works

### 1. Human Verification
Users prove they're human by showing three simple hand gestures:
- ✌️ **Peace sign**
- **3️⃣ Number three**
- 👍 **Thumbs up**

### 2. Gesture-Based Password
After verification, users enter a password using binary hand gestures. The default password requires showing finger combinations that represent the numbers **3**, **17**, and **2** in sequence.

The system converts finger positions into binary numbers by detecting which fingers are extended, creating a unique and intuitive way to enter passwords without a keyboard.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python / Flask** | Web server and API endpoints |
| **OpenCV** | Video capture and image processing |
| **MediaPipe** | Real-time hand landmark detection |
| **TailwindCSS** | Frontend styling |
| **Server-Sent Events** | Live gesture updates to the browser |

## Key Features

- 🎥 **Real-time video processing** with live webcam feed
- 🤖 **ML-powered hand tracking** using Google's MediaPipe
- 🔢 **Binary gesture encoding** - fingers map to binary digits
- ⚡ **Live updates** via Server-Sent Events
- 🎨 **Clean UI** with TailwindCSS

## The Math Behind It

Each finger represents a binary bit:
- Thumb = 1
- Index = 2
- Middle = 4
- Ring = 8
- Pinky = 16

So "thumbs up" (only thumb extended) = **1**, and "peace sign" (index + middle) = **6**.

The system calculates the distance of each fingertip from the palm center to determine if a finger is extended or curled.

## Running Locally

### Prerequisites
- Python 3.x
- Webcam

### Setup

```bash
# Install Python dependencies
pip install flask opencv-python mediapipe numpy

# Install frontend dependencies (optional, for TailwindCSS development)
npm install

# Run the application
python app.py
```

Then open `http://localhost:5000` in your browser and allow camera access.

## Why I Built This

Traditional CAPTCHAs are frustrating and often inaccessible. I wanted to explore an alternative that:
- Uses natural human gestures
- Provides immediate visual feedback
- Demonstrates practical computer vision applications
- Is actually fun to use!

---

*Built with 🖐️ by Jaiman*
