# Gesture Control Keyboard

A Python-based virtual keyboard controlled using hand gestures. This project leverages MediaPipe's modern Hand Landmarker solution to track hand movements and simulate keyboard inputs.

## Features
- **Hand Tracking:** Uses MediaPipe Hand Landmarker for fast and accurate hand tracking.
- **Gesture Control:** Type or trigger keyboard events purely using hand gestures via your webcam.
- **Configurable:** Settings and key mappings can be easily adjusted via `config.json`.

## Project Structure
- `main.py`: The entry point of the application. It captures webcam feed, processes hand landmarks, and handles keyboard events.
- `utils.py`: Helper functions for gesture recognition, calculations, or UI drawing.
- `config.json`: Configuration file for adjusting sensitivity, key bindings, or webcam settings.
- `hand_landmarker.task`: The pre-trained MediaPipe machine learning model used to detect hand landmarks.

## Prerequisites

Before running the project, ensure you have Python installed and install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui
