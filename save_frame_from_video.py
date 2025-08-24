import cv2

VIDEO_PATH = 'carPark.mp4'

cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Could not read a frame from the video. Check VIDEO_PATH.")
cv2.imwrite('carParkImg.png', frame)
print("Saved carParkImg.png from first frame of", VIDEO_PATH)
