import cv2
import numpy as np
import pickle
import cvzone

# === CONFIG ===
# Set to True to use webcam instead of video file
USE_WEBCAM = False  # change to True if you want to use your webcam
VIDEO_PATH = 'carPark.mp4'
WIDTH, HEIGHT = 107, 48     # parking spot box size
THRESHOLD = 900             # tune per scene; lower = more likely to be "empty"

# === CAPTURE ===
if USE_WEBCAM:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
else:
    cap = cv2.VideoCapture(VIDEO_PATH)

# === LOAD SLOT POSITIONS ===
with open('parkingSlotPositions.npy', 'rb') as f:
    posList = pickle.load(f)

def checkSpaces(frame, imgPro):
    free = 0
    for idx, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgPro[y:y + HEIGHT, x:x + WIDTH]
        count = cv2.countNonZero(imgCrop)

        if count < THRESHOLD:
            color = (0, 255, 0)  # free
            free += 1
        else:
            color = (0, 0, 255)  # occupied

        cv2.rectangle(frame, (x, y), (x + WIDTH, y + HEIGHT), color, 2)
        cv2.putText(frame, str(idx + 1), (x + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

    cvzone.putTextRect(frame, f'Free: {free}/{len(posList)}', (30, 50), scale=2, thickness=2, offset=10, colorR=(0, 200, 0))
    return frame

while True:
    if not cap.isOpened():
        break
    ret, img = cap.read()
    if not ret:
        # Loop the video when using a file
        if not USE_WEBCAM:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        else:
            break

    # Preprocess
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    out = checkSpaces(img, imgDilate)

    cv2.imshow('Parking Counter', out)
    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
