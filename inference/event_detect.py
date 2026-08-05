from ultralytics import YOLO
import cv2
import time
import os
import math
from collections import deque

# ---------------- CONFIG ----------------
MODEL_PATH = "runs/results/runs/detect/train/weights/best.pt"
VIDEO_PATH = "5.mp4"
EVIDENCE_DIR = "evidence"

DISTANCE_THRESHOLD = 500
NEW_WASTE_DISTANCE = 60
WALK_AWAY_THRESHOLD = 40
PERSON_MISSING_DELAY = 1.5
POST_LEAVE_WASTE_SECONDS = 4
COOLDOWN_SECONDS = 8

FPS_ASSUMED = 20
BUFFER_SECONDS = 5

os.makedirs(EVIDENCE_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

# ---------------- STATE ----------------
previous_waste_centers = []
person_last_seen_time = {}

candidate = None
last_event_time = 0

# ---------------- HELPERS ----------------
def center(x1, y1, x2, y2):
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def save_case(person_crop, waste_frame, timestamp):
    case_folder = os.path.join(EVIDENCE_DIR, f"case_{timestamp}")
    os.makedirs(case_folder, exist_ok=True)

    cv2.imwrite(os.path.join(case_folder, "person.jpg"), person_crop)
    cv2.imwrite(os.path.join(case_folder, "waste.jpg"), waste_frame)

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")
    boxes = results[0].boxes

    persons = []
    wastes = []

    # -------- Collect Detections --------
    if boxes is not None:
        for box in boxes:
            cls = int(box.cls[0])
            track_id = int(box.id[0]) if box.id is not None else None
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if cls == 0:  # person
                persons.append((track_id, x1, y1, x2, y2))
                person_last_seen_time[track_id] = current_time

            elif cls == 1:  # waste
                wastes.append((x1, y1, x2, y2))

    current_waste_centers = [
        center(x1, y1, x2, y2) for (x1, y1, x2, y2) in wastes
    ]

    # ---------------- DETECT NEW WASTE ----------------
    if persons and wastes and candidate is None:

        for (x1, y1, x2, y2), waste_center in zip(wastes, current_waste_centers):

            is_new = True
            for prev in previous_waste_centers:
                if distance(waste_center, prev) < NEW_WASTE_DISTANCE:
                    is_new = False
                    break

            if not is_new:
                continue

            # Find closest person
            closest_person = min(
                persons,
                key=lambda p: distance(
                    waste_center,
                    center(p[1], p[2], p[3], p[4])
                )
            )

            pid, px1, py1, px2, py2 = closest_person
            person_center = center(px1, py1, px2, py2)

            if distance(waste_center, person_center) < DISTANCE_THRESHOLD:

                # SIMPLE FIX: Capture best person image NOW
                margin = 20
                crop_x1 = max(0, px1 - margin)
                crop_y1 = max(0, py1 - margin)
                crop_x2 = min(frame.shape[1], px2 + margin)
                crop_y2 = min(frame.shape[0], py2 + margin)

                person_crop = frame[crop_y1:crop_y2, crop_x1:crop_x2].copy()

                candidate = {
                    "person_id": pid,
                    "waste_pos": waste_center,
                    "left_time": None,
                    "person_image": person_crop
                }
                break

    # ---------------- TRACK CANDIDATE ----------------
    if candidate is not None:

        # Check waste still exists
        waste_still_present = any(
            distance(candidate["waste_pos"], wc) < NEW_WASTE_DISTANCE
            for wc in current_waste_centers
        )

        if not waste_still_present:
            candidate = None
            continue

        tracked_person = next(
            (p for p in persons if p[0] == candidate["person_id"]),
            None
        )

        person_left = False

        if tracked_person:
            _, px1, py1, px2, py2 = tracked_person
            current_center = center(px1, py1, px2, py2)

            if distance(current_center, candidate["waste_pos"]) > WALK_AWAY_THRESHOLD:
                person_left = True
        else:
            last_seen = person_last_seen_time.get(candidate["person_id"], 0)
            if current_time - last_seen > PERSON_MISSING_DELAY:
                person_left = True

        if person_left and candidate["left_time"] is None:
            candidate["left_time"] = current_time

        if candidate["left_time"] is not None:

            if (
                current_time - candidate["left_time"] >= POST_LEAVE_WASTE_SECONDS and
                current_time - last_event_time > COOLDOWN_SECONDS
            ):

                timestamp = int(current_time)

                # Use stored clean person image
                person_crop = candidate["person_image"]

                waste_frame = frame.copy()

                save_case(person_crop, waste_frame, timestamp)

                print("🚨 Illegal Dumping Confirmed")

                last_event_time = current_time
                candidate = None

    previous_waste_centers = current_waste_centers.copy()

    annotated = results[0].plot()
    cv2.imshow("Illegal Dump Detection", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()