# 🖐️ ARM — Touchless Hand Gesture Media Controller

> A real-time, touchless media control system using computer vision and hand gesture recognition. Built for the **Bharat AI Challenge PS2**.

---

## 📖 Overview

**ARM** is a Python-based application that lets you control your media player — play/pause, volume, fast-forward, rewind, fullscreen, and more — entirely through hand gestures captured by your webcam. No mouse. No keyboard. No touch.

It uses **Google MediaPipe** for 21-point hand landmark detection and a custom rule-based gesture classifier optimized for edge devices (no heavy ML models).

---

## ✨ Features

- 🖐️ **Dual-Hand Control** — Left hand handles playback & screen; right hand handles navigation & volume
- ⚡ **Multithreaded Camera Input** — Decoupled frame capture for higher, stable FPS
- 🎯 **User Calibration** — Personalized gesture thresholds saved to a local profile
- 📊 **Session Benchmarking** — Auto-generates FPS/latency charts and CSV reports on exit
- 🧠 **Zero Heavy ML** — Runs on CPU-only, edge-device friendly (no GPU required)
- 🛑 **Gesture Exit** — Cleanly shut down the program using a hand gesture

---

## 🖐️ Gesture Command Map

### Left Hand (Playback & Screen Control)

| Gesture | Action |
|---|---|
| ✋ Open Palm | ▶️ / ⏸️ Play / Pause |
| ✊ Fist | 🔲 Toggle Fullscreen |
| ☝️ 1 Finger (Index) | ⏪ Rewind |
| 🤟 Thumb + Index + Middle | 🛑 Exit Program |

### Right Hand (Navigation & Volume)

| Gesture | Action |
|---|---|
| ☝️ 1 Finger (Index) | ⏩ Fast Forward |
| ✌️ 2 Fingers | 🔊 Volume Up |
| 🤞 3 Fingers | 🔉 Volume Down |
| ✊ Fist | 🔇 Mute / Unmute |

---

## 🗂️ Project Structure

```
ARM/
├── main.py              # Entry point — camera loop, gesture pipeline, session reporting
├── classifier.py        # GestureDetector — rule-based hand shape classifier
├── media_controller.py  # MediaController — maps gestures to keyboard actions (pyautogui)
├── hud.py               # HUDOverlay — renders transparent FPS/confidence/history dashboard
├── calibration.py       # CalibrationManager — personalized threshold training & profile I/O
├── benchmark.py         # generate_report_files() — saves results.csv & benchmark_charts.png
├── result/              # Auto-generated output folder (CSV + PNG reports)
├── Figure_1.png         # Sample output figure
└── benchmark_charts.png # Sample benchmark chart
```

---

## 🛠️ Requirements

- Python **3.8+**
- A working **webcam**

### Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui matplotlib numpy
```

---

## 🚀 Usage

### 1. Run Normally (with default thresholds)

```bash
python main.py
```

### 2. Run with Personal Calibration (Recommended)

Run calibration once to train gesture thresholds to your hand size and lighting:

```bash
python main.py --calibrate
```

Follow the on-screen instructions (show **Open Palm**, then **Fist**). Your profile is saved to `profile.json` and auto-loaded on future runs.

### 3. Exit

- Show the **Left Hand Thumb + Index + Middle** gesture, **or**
- Press **`q`** on your keyboard

---

## 📊 Benchmark Reports

After every session, reports are automatically saved to the `result/` folder:

| File | Description |
|---|---|
| `result/results.csv` | Per-frame timestamp, latency (ms), and FPS |
| `result/benchmark_charts.png` | FPS line chart + Latency distribution histogram |

A terminal summary is also printed:

```
============================================================
📊 BHARAT AI CHALLENGE PS2 - SHORT REPORT
============================================================
⚙️  SYSTEM DESIGN:
   - Multithreaded Camera Input for decoupled processing
   - Dual-Hand Split Control (Left: Playback, Right: Navigation)

🧠 MODEL & RULE SELECTION:
   - MediaPipe Hands for 21-point landmark detection
   - Pure Python Rule-Based Logic (Finger counting)
   - Zero heavy ML models used to ensure edge-device optimization

🚀 PERFORMANCE METRICS:
   - Average Frame Rate: 28.4 FPS  (Target: >= 15 FPS)
   - Average Latency:    35.2 ms   (Target: < 200 ms)
   - Est. Accuracy:      > 90%
============================================================
```

---

## ⚙️ How It Works

```
Webcam Frame
    │
    ▼
CameraThread (Background Thread)
    │  Captures frames continuously to avoid blocking the main loop
    ▼
MediaPipe Hands
    │  Detects 21 hand landmarks per hand in real-time
    ▼
GestureDetector (classifier.py)
    │  Classifies hand shape using finger tip vs. knuckle Y-position
    │  Identifies Left vs. Right hand by wrist X-position
    ▼
MediaController (media_controller.py)
    │  Maps gesture → keyboard shortcut via pyautogui
    │  Applies per-gesture cooldown timers to prevent repeated triggers
    ▼
HUDOverlay (hud.py)
    │  Renders semi-transparent FPS, confidence, gesture history on frame
    ▼
cv2.imshow → Live Window
```

---

## 🏆 Performance Targets

| Metric | Target | Typical Result |
|---|---|---|
| Frame Rate | ≥ 15 FPS | ~25–35 FPS |
| End-to-End Latency | < 200 ms | ~30–60 ms |
| Gesture Accuracy | > 90% | > 90% (strict static shape logic) |

---

## 📄 License

This project was developed for academic and competition purposes as part of the **Bharat AI Challenge PS2**.

---

*Built with ❤️ using MediaPipe, OpenCV, and Python.*
