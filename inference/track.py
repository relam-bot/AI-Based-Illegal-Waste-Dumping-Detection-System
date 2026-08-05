from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("runs/detect/train4/weights/best.pt")

# Start webcam
cap = cv2.VideoCapture("video4.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection + ByteTrack tracking
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")

    # Show result
    annotated = results[0].plot()
    cv2.imshow("YOLOv8 ByteTrack", annotated)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
