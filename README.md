# Doctor Strange – AI Magic Hand Tracking (V2)

A real-time computer-vision experiment that maps hand gestures to stylized magical visual effects.

## Features
- Real-time hand landmark tracking with MediaPipe
- Tracks up to two hands
- Open palm gesture: animated magic-shield circle
- Index-finger-only gesture: glowing spell trail
- Floating particle effects
- On-screen status HUD

## Tech stack
- Python 3.11
- OpenCV
- MediaPipe
- NumPy

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, allow scripts for this terminal session only:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Controls
- Show an open palm to display the magic shield.
- Raise only the index finger to draw a glowing trail.
- Press `Q` in the camera window to quit.

## Notes
- Allow camera access for your terminal/VS Code.
- Close other applications that may be using the webcam.
- Visual effects are a creative overlay; gesture detection is performed locally.

## Project structure
```text
Doctor-Strange-AI-Magic-Tracking/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
