import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Press 's' to save frame as carParkImg.png, 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    cv2.imshow('Webcam - press s to save', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite('carParkImg.png', frame)
        print("Saved carParkImg.png")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
