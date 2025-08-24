import cv2
import pickle

# Box size for each parking spot (tune if needed)
width, height = 107, 48

# Load previously saved positions (if any)
try:
    with open('parkingSlotPositions.npy', 'rb') as f:
        posList = pickle.load(f)
except Exception:
    posList = []

def mouseClick(events, x, y, flags, params):
    global posList
    # Left-click: add a spot
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    # Right-click: remove the spot you right-click inside
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break
    # Persist after each change
    with open('parkingSlotPositions.npy', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('carParkImg.png')
    if img is None:
        raise FileNotFoundError("carParkImg.png not found. Generate it from video or webcam first.")
    # Draw current boxes and their indices
    for idx, pos in enumerate(posList):
        x, y = pos
        cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 255), 2)
        cv2.putText(img, str(idx + 1), (x + 5, y + 20), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

    cv2.putText(img, "Left-click=Add, Right-click=Remove, q=Quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow('Select Parking Spaces', img)
    cv2.setMouseCallback('Select Parking Spaces', mouseClick)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
