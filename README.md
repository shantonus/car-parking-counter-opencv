# Car Parking Space Counter (OpenCV + Python)

A beginner-friendly project that detects **free vs occupied** parking spaces from a top-down video or live webcam feed.

## ✨ Features
- Manual selection of parking spots using the mouse
- Counts **Free / Total** spots live
- Works with a **video file** or **webcam**
- Clean on-screen UI (via `cvzone`) and easy-to-tune threshold

---

## 🧰 Tech Stack
- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- cvzone

---

## 📂 Project Structure
```
car_parking_counter/
├── ParkingCounter.py            # Main app: processes frames and counts spots
├── SelectParkingSpaces.py       # Manual tool to mark parking spaces
├── save_frame_from_video.py     # Helper: save first video frame to carParkImg.png
├── capture_from_webcam.py       # Helper: save a webcam frame to carParkImg.png
├── carPark.mp4                  # (Add your own) source video
├── carParkImg.png               # Generated frame for selecting spots
├── parkingSlotPositions.npy     # Saved/loaded spots (auto-created)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

1) **Install dependencies**
```bash
pip install -r requirements.txt
```

2) **Prepare a reference image**
- If using a **video**:
  ```bash
  python save_frame_from_video.py
  ```
- If using a **webcam**, run and press `s` to save a frame:
  ```bash
  python capture_from_webcam.py
  ```

3) **Mark parking spots** (left-click add, right-click remove, `q` quit)
```bash
python SelectParkingSpaces.py
```

4) **Run the counter**
```bash
python ParkingCounter.py
```

---

## 🎛️ Configuration

In `ParkingCounter.py`:
- Switch input source:
  ```python
  USE_WEBCAM = False  # True to use webcam
  VIDEO_PATH = 'carPark.mp4'
  ```
- Box size for spots: `WIDTH, HEIGHT = 107, 48`
- Occupancy threshold: `THRESHOLD = 900` (tune for your scene)

---

## 🧪 How It Works (Pipeline)
1. Read frame (video/webcam)
2. Grayscale → Blur → Adaptive Threshold → Median Blur → Dilate
3. For each marked spot, crop & count non-zero pixels
4. If `count < THRESHOLD` → **Free** (green); else **Occupied** (red)
5. Draw boxes & show `Free / Total`

---

## ⛑️ Troubleshooting
- **Boxes misaligned?** Recreate `carParkImg.png` from the **same source** used at runtime.
- **Wrong total/free count?**
  - Delete and recreate `parkingSlotPositions.npy`
  - Tune the `THRESHOLD` value
- **Quit app:** Press `q` in the window.

---

## 📄 License
MIT License — see `LICENSE`.
