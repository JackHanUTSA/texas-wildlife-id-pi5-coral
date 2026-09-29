# Training / Fine-tuning for Texas Wildlife

## Dataset
Collect IR images of Texas species. Use iNaturalist Texas filter, TPWD datasets, and field captures.

## Recommended Model
YOLOv8n or MobileNetV2 SSD. Convert to TFLite and compile for Edge TPU.

## Steps
1. Prepare dataset in YOLO format:
   /dataset/images/train
   /dataset/labels/train

2. Train:
   yolo train model=yolov8n.pt data=data.yaml epochs=100 imgsz=320

3. Export to TFLite:
   yolo export model=best.pt format=tflite imgsz=320

4. Compile for Edge TPU:
   edgetpu_compiler wildlife.tflite

Result: wildlife_edgetpu.tflite

## Transfer Learning
Use pre-trained COCO weights and fine-tune on Texas species for faster convergence.
