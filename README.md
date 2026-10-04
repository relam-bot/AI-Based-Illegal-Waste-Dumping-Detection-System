# 🛡️ Green Guard — AI-Based Illegal Dumping Detection System

Green Guard is an AI-powered computer vision system designed to detect **people and waste in CCTV/webcam footage** and form the foundation for an automated illegal-dumping detection system.

The current implementation focuses on the **object detection stage** using **YOLOv8n**. The system detects:

- 👤 `person`
- 🗑️ `waste_bag`

The project is designed to be extended with **object tracking, illegal-dumping event detection, evidence collection, alerts, and a monitoring dashboard**.

---

## 📌 Project Overview

Illegal dumping of waste in public areas is a major environmental and sanitation problem. Traditional CCTV systems can record these incidents, but they generally require a person to continuously monitor the footage.

Green Guard aims to automate this process using computer vision.

### Current Pipeline

```text
CCTV / Webcam / Video
          │
          ▼
     YOLOv8n Model
          │
          ▼
 ┌───────────────────┐
 │ Object Detection  │
 └───────────────────┘
          │
     ┌────┴─────┐
     ▼          ▼
  Person     Waste Bag
     │          │
     └────┬─────┘
          ▼
   Future Event Detection
          │
          ▼
   Illegal Dumping Event
          │
          ▼
 Evidence + Alert + Dashboard
```

---

# 🚀 Current Features

### Implemented

- YOLO-based object detection
- Person detection
- Waste-bag detection
- Custom dataset training
- GPU-accelerated training using CUDA
- Webcam inference
- Image/video inference
- Adjustable confidence threshold
- Detection visualization with bounding boxes

### Planned

- Person and waste tracking
- ByteTrack / DeepSORT integration
- Temporal event detection
- Illegal dumping classification
- Automatic evidence snapshots
- Video evidence recording
- Timestamp generation
- GPS/geolocation information
- Automated alerts
- Database storage
- Web dashboard
- CCTV deployment

---

# 🧠 Model

The current model is:

**YOLOv8n**

YOLOv8n was selected because Green Guard is intended to eventually operate on real-time CCTV/video streams.

### Why YOLOv8n?

Compared with larger YOLO models, YOLOv8n provides:

- Faster inference
- Lower GPU memory requirements
- Better suitability for real-time applications
- Easier deployment on lower-end hardware

The current development machine uses:

```text
GPU: NVIDIA GeForce GTX 1650
VRAM: 4 GB
```

Therefore, YOLOv8n provides a practical balance between detection accuracy and inference speed.

---

# 🗂️ Dataset

The current dataset is located at:

```text
C:/dump/data/waste1/
```

The expected dataset structure is:

```text
waste1/
│
├── data.yaml
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
└── test/
    ├── images/
    └── labels/
```

The current dataset contains approximately:

```text
39,000 images
```

The active dataset configuration uses two classes:

```yaml
nc: 2

names:
  - person
  - waste_bag
```

### `data.yaml`

Example:

```yaml
train: train/images
val: valid/images
test: test/images

nc: 2

names:
  - person
  - waste_bag
```

---

# 💻 Requirements

## Hardware

Recommended development hardware:

```text
GPU: NVIDIA GPU with CUDA support
RAM: 16 GB or more
Storage: SSD recommended
```

The project was developed/tested using:

```text
GPU: NVIDIA GeForce GTX 1650 4GB
```

---

# 🐍 Software Requirements

Recommended environment:

```text
Python 3.10
PyTorch 2.7.1 + CUDA 11.8
Ultralytics 8.3.235
```

The project uses a Conda environment named:

```text
dump_env
```

---

# ⚙️ Environment Setup

## 1. Create the Conda environment

If the environment does not already exist:

```bash
conda create -n dump_env python=3.10
```

Activate it:

```bash
conda activate dump_env
```

---

## 2. Install PyTorch

For the current CUDA configuration:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 3. Install Ultralytics

```bash
pip install ultralytics
```

---

# 🔍 Verify GPU

Before training, verify that PyTorch can access the NVIDIA GPU.

Run:

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Expected output should be similar to:

```text
True NVIDIA GeForce GTX 1650
```

If it returns:

```text
False
```

the model will not use the NVIDIA GPU.

---

# 🏋️ Training the Model

Activate the environment:

```bash
conda activate dump_env
```

Then run:

```bash
yolo task=detect mode=train model=yolov8n.pt data=C:/dump/data/waste1/data.yaml epochs=10 imgsz=512 batch=4 device=0 workers=2 val=True
```

---

# 📋 Training Parameters

| Parameter | Value | Purpose |
|---|---:|---|
| `task` | `detect` | Object detection |
| `mode` | `train` | Training mode |
| `model` | `yolov8n.pt` | YOLOv8 Nano pretrained model |
| `data` | `data.yaml` | Dataset configuration |
| `epochs` | `10` | Number of training epochs |
| `imgsz` | `512` | Input image size |
| `batch` | `4` | Batch size |
| `device` | `0` | First CUDA GPU |
| `workers` | `2` | Data-loading workers |
| `val` | `True` | Run validation |

### Adjusting batch size

If GPU memory becomes insufficient:

```bash
batch=2
```

or:

```bash
batch=1
```

If sufficient GPU memory is available, a larger batch size may improve training throughput.

---

# 📁 Training Output

Ultralytics normally creates a run directory similar to:

```text
runs/
└── detect/
    └── train/
        ├── weights/
        │   ├── best.pt
        │   └── last.pt
        │
        ├── results.csv
        ├── results.png
        ├── confusion_matrix.png
        └── ...
```

Depending on previous training runs, the directory may instead be:

```text
train2/
train3/
train4/
...
```

The most important files are:

### `best.pt`

The best-performing checkpoint during training.

### `last.pt`

The checkpoint from the final training epoch.

For inference, normally use:

```text
best.pt
```

---

# 🎥 Webcam Detection

After training, you can run the model on a webcam.

Example:

```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=0 conf=0.25 show=True
```

Here:

```text
source=0
```

usually refers to the default webcam.

If the camera does not work, try:

```bash
source=1
```

or:

```bash
source=2
```

---

# 🎯 Confidence Threshold

The confidence threshold controls how confident the model must be before displaying a detection.

Example:

```bash
conf=0.25
```

### Lower confidence

```bash
conf=0.20
```

Produces more detections but may increase false positives.

### Higher confidence

```bash
conf=0.50
```

Produces fewer detections but can reduce false positives.

For testing:

```text
0.20 – 0.30
```

is a reasonable starting range.

For final deployment, the threshold should be selected using validation/testing results.

---

# 🖼️ Image Detection

To test the model on an image:

```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source="image.jpg" conf=0.25
```

Example:

```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source="test.jpg" conf=0.25
```

---

# 🎞️ Video Detection

The model can also process a video:

```bash
yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source="video.mp4" conf=0.25
```

This provides the foundation for future CCTV processing.

---

# 📹 CCTV Integration

A future deployment can connect the detection system to an RTSP CCTV stream.

Conceptually:

```text
CCTV Camera
     │
     ▼
RTSP Stream
     │
     ▼
Green Guard
     │
     ▼
YOLOv8n
     │
     ▼
Person + Waste Detection
     │
     ▼
Event Detection
```

The exact RTSP URL depends on the CCTV/NVR configuration.

---

# 🚨 Illegal Dumping Detection

Object detection alone does **not** prove that illegal dumping has occurred.

For example:

```text
Person + Waste
```

does not necessarily mean:

```text
Illegal Dumping
```

A person may simply be walking while carrying a bag.

Therefore, the next stage is **event detection**.

---

## Planned Event Detection Logic

A future version can use temporal information:

```text
Person detected
       │
       ▼
Waste detected
       │
       ▼
Person approaches waste area
       │
       ▼
Person remains near area
       │
       ▼
Waste is placed/released
       │
       ▼
Person leaves
       │
       ▼
Illegal dumping event
```

This is why object tracking and temporal reasoning are important.

---

# 👁️ Future Tracking

A tracker such as:

```text
ByteTrack
```

or:

```text
DeepSORT
```

can assign IDs to detected objects.

Example:

```text
Person #12
Person #18
Waste #4
Waste #7
```

This allows the system to understand how objects move across multiple video frames.

---

# 🧩 Future System Architecture

The complete Green Guard system is planned to contain:

```text
                    ┌───────────────────┐
                    │ CCTV / Webcam     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Frame Processing   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ YOLOv8 Detection   │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
                 Person               Waste
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ Object Tracking    │
                    │   ByteTrack /      │
                    │    DeepSORT        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Event Detection    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Illegal Dumping?   │
                    └─────────┬─────────┘
                              │
                         ┌────┴────┐
                         │         │
                        YES        NO
                         │         │
                         ▼         ▼
                   Evidence     Continue
                   Collection   Monitoring
                         │
                         ▼
                ┌────────────────────┐
                │ Database / Storage │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Alert / Dashboard  │
                └────────────────────┘
```

---

# 📸 Future Evidence Collection

When an illegal-dumping event is confirmed, the system can automatically capture:

```text
Image
Timestamp
Camera ID
Location
Person bounding box
Waste bounding box
Event confidence
```

Example:

```text
Event ID: GG-00021
Date: 2026-XX-XX
Time: 18:32:15
Camera: CAM-03
Event: Illegal Dumping
Confidence: 91%
```

---

# 🗄️ Future Database

A database can store detected events.

Example structure:

```text
dumping_events
│
├── id
├── timestamp
├── camera_id
├── location
├── event_type
├── confidence
├── image_path
├── video_path
└── status
```

Possible statuses:

```text
Detected
Verified
Reported
Resolved
False Positive
```

---

# 📊 Future Dashboard

The final system can contain a web dashboard showing:

```text
┌─────────────────────────────────────────┐
│           GREEN GUARD DASHBOARD         │
├─────────────────────────────────────────┤
│                                         │
│  Total Events       Today       Cameras │
│      124              7            12   │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│          LIVE CCTV FEED                 │
│                                         │
│       ┌─────────────────────┐           │
│       │                     │           │
│       │     CAMERA 03       │           │
│       │                     │           │
│       └─────────────────────┘           │
│                                         │
├─────────────────────────────────────────┤
│ Recent Events                           │
│                                         │
│ 18:32  Illegal Dumping   CAM-03         │
│ 17:41  Illegal Dumping   CAM-07         │
│ 16:20  False Positive    CAM-02         │
│                                         │
└─────────────────────────────────────────┘
```

---

# ⚠️ Dataset Warning

Some versions of the dataset may contain both detection and segmentation annotations.

Ultralytics can display a warning similar to:

```text
Box and segment counts should be equal...
```

This means the dataset contains a mixture of bounding-box and segmentation annotations.

For this project, the model is being trained as an **object detection model**, so the dataset should ideally contain only:

```text
Images
+
YOLO bounding-box labels
```

A clean detection dataset is recommended for the final version.

---

# 🛠️ Windows Command-Line Notes

If using:

```text
Command Prompt
```

or:

```text
Anaconda Prompt
```

commands should normally be entered on a single line.

For example:

```bash
yolo task=detect mode=train model=yolov8n.pt data=C:/dump/data/waste1/data.yaml epochs=10 imgsz=512 batch=4 device=0 workers=2 val=True
```

Do **not** use:

```text
\
```

as a line continuation character.

If you want to split a command across multiple lines in Windows CMD, use:

```text
^
```

---

# 🔧 Troubleshooting

## CUDA is False

Run:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If it returns:

```text
False
```

check:

- NVIDIA driver
- PyTorch CUDA installation
- Active Conda environment
- GPU availability

Make sure:

```bash
conda activate dump_env
```

is executed before running the model.

---

## Webcam Does Not Open

Try:

```bash
source=0
```

then:

```bash
source=1
```

and:

```bash
source=2
```

Another application may also be using the webcam.

---

## CUDA Out of Memory

Reduce the batch size:

```bash
batch=2
```

or:

```bash
batch=1
```

You can also reduce the image size:

```bash
imgsz=416
```

---

## Detection Has Too Many False Positives

Increase confidence:

```bash
conf=0.40
```

or:

```bash
conf=0.50
```

However, confidence should ultimately be selected using validation results rather than arbitrary tuning.

---

# 📈 Model Evaluation

Important metrics for evaluating the detection model include:

```text
Precision
Recall
mAP@50
mAP@50-95
Confusion Matrix
Inference Speed
```

For an illegal-dumping detection system, both **false positives and false negatives** are important.

A model that detects every possible waste object but produces many false alarms may not be suitable for real-world deployment.

---

# 🔬 Development Roadmap

## Phase 1 — Object Detection

- [x] Dataset preparation
- [x] Dataset configuration
- [x] YOLO model selection
- [x] GPU training environment
- [x] Person detection
- [x] Waste detection
- [ ] Final model evaluation

## Phase 2 — Tracking

- [ ] ByteTrack
- [ ] Object IDs
- [ ] Track persistence
- [ ] Person-waste association

## Phase 3 — Event Detection

- [ ] Temporal reasoning
- [ ] Person approaching waste
- [ ] Waste placement detection
- [ ] Person leaving
- [ ] Illegal-dumping event confirmation

## Phase 4 — Evidence

- [ ] Automatic snapshots
- [ ] Video clips
- [ ] Timestamp
- [ ] Camera ID
- [ ] Location metadata

## Phase 5 — Alerts

- [ ] Email alerts
- [ ] Notification system
- [ ] Event severity
- [ ] False-positive handling

## Phase 6 — Dashboard

- [ ] Live CCTV feed
- [ ] Event history
- [ ] Evidence viewer
- [ ] Statistics
- [ ] Camera management

## Phase 7 — Deployment

- [ ] Real CCTV integration
- [ ] Performance optimization
- [ ] Edge deployment
- [ ] Long-duration testing

---

# 📁 Suggested Project Structure

The final project can be organized as:

```text
GreenGuard/
│
├── data/
│   └── waste1/
│       ├── train/
│       ├── valid/
│       ├── test/
│       └── data.yaml
│
├── models/
│   └── best.pt
│
├── detection/
│   └── detector.py
│
├── tracking/
│   └── tracker.py
│
├── event_detection/
│   └── dumping_detector.py
│
├── evidence/
│   └── evidence_manager.py
│
├── database/
│   └── database.py
│
├── dashboard/
│   └── app.py
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

The current implementation does not require all of these modules yet. They represent the planned final architecture.

---

# ▶️ Quick Start

For someone who already has the environment configured:

### 1. Activate environment

```bash
conda activate dump_env
```

### 2. Train

```bash
yolo task=detect mode=train model=yolov8n.pt data=C:/dump/data/waste1/data.yaml epochs=10 imgsz=512 batch=4 device=0 workers=2 val=True
```

### 3. Locate the trained model

```text
runs/detect/<run_name>/weights/best.pt
```

### 4. Run webcam detection

```bash
yolo task=detect mode=predict model=runs/detect/<run_name>/weights/best.pt source=0 conf=0.25 show=True
```

### 5. Test an image

```bash
yolo task=detect mode=predict model=runs/detect/<run_name>/weights/best.pt source="test.jpg" conf=0.25
```

---

# 📚 Technologies Used

- **Python**
- **YOLOv8**
- **Ultralytics**
- **PyTorch**
- **CUDA**
- **OpenCV**
- **Roboflow / Custom Dataset**
- **Conda**

Future components may include:

- ByteTrack / DeepSORT
- FastAPI / Flask
- SQLite / Firebase
- Streamlit
- Email/notification APIs

---

# 🎯 Project Goal

The ultimate goal of Green Guard is not simply to detect waste.

The goal is to build an intelligent system capable of determining:

> **Who is interacting with the waste, what happened, whether the behavior constitutes illegal dumping, and how to automatically produce useful evidence.**

The current YOLOv8n detector is therefore the **first stage of a larger intelligent surveillance pipeline**.

---

# 👨‍💻 Project Status

**Current Stage:**

```text
Object Detection Development
```

**Current Model:**

```text
YOLOv8n
```

**Current Classes:**

```text
person
waste_bag
```

**Target System:**

```text
Real-Time Illegal Dumping Detection
```

---

# 📜 License

This project is intended for academic and research purposes.

Model, dataset, and third-party components remain subject to their respective licenses and usage terms.
