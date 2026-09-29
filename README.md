# Texas Wildlife Identification System

Real-time wild animal identification for Texas using Raspberry Pi 5 + infrared camera + Google Coral Edge TPU.

## Hardware
- Raspberry Pi 5
- Pi Camera Module 3 with NoIR filter or IR cut filter removed + IR illuminator
- Google Coral Edge TPU USB Accelerator
- Solar panel + charge controller + LiFePO4 battery backup
- 4G/5G SIM card modem / USB dongle
- Servo/stepper motor for trap/trigger/LED
- Optional: IR LED ring for night vision

## Software Stack
- Python 3.11+
- Picamera2
- OpenCV
- TensorFlow Lite 2.15+ with Coral runtime
- Edge TPU compiler

## Supported Texas Species
white-tailed deer, mule deer, coyote, gray fox, bobcat, mountain lion, javelina, armadillo, raccoon, opossum, striped skunk, feral hog, turkey, quail, etc.

## Quick Start
```bash
cd texas_wildlife_id
pip install -r requirements.txt
python src/main.py --config config.yaml
```

Configure `config.yaml` for:
- `power`: solar/battery monitoring
- `cellular`: SIM modem APN and receiver URL for image upload
- `motor`: GPIO pin and trigger classes for auto-trigger

## Project Structure
```
texas_wildlife_id/
├─ src/
│  ├─ capture.py      # Picamera2 IR capture
│  ├─ inference.py    # Coral TPU inference
│  ├─ main.py         # Pipeline
│  └─ utils.py
├─ models/
├─ logs/
└─ config.yaml
```

## Notes
Model training/fine-tuning instructions in docs/training.md
