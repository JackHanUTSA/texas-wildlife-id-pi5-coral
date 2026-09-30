import yaml
import argparse
import cv2
import os
import time
from datetime import datetime
from src.capture import IRCamera
from src.inference import CoralInference
from src.utils import ensure_dirs, timestamp
from src.power import PowerManager
from src.cellular import CellularUploader
from src.motor import MotorTrigger
from src.climate import ClimateSensor
from src.fan import FanController

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml')
    parser.add_argument('--model', default=None)
    parser.add_argument('--labels', default=None)
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    if args.model:
        cfg['inference']['model_path'] = args.model
    if args.labels:
        cfg['inference']['labels_path'] = args.labels

    ensure_dirs(cfg)
    
    cam = IRCamera(cfg['camera'])
    infer = CoralInference(cfg['inference']['model_path'], cfg['inference']['labels_path'], cfg['inference']['input_size'])
    power = PowerManager(cfg['power']['low_battery_threshold'], cfg['power'].get('battery_monitor_pin'))
    cellular = CellularUploader(cfg['cellular']['receiver_url'], cfg['cellular'].get('apn'), cfg['cellular'].get('modem_device')) if cfg['cellular']['enabled'] else None
    motor = MotorTrigger(cfg['motor']['gpio_pin'], cfg['motor']['trigger_duration_sec'], cfg['motor']['cooldown_sec']) if cfg['motor']['enabled'] else None
    climate = ClimateSensor(cfg['climate']['sensor_type'], cfg['climate']['i2c_bus'], cfg['climate']['address']) if cfg['climate']['enabled'] else None
    fan = FanController(cfg['fan']['gpio_pin'], cfg['fan']['pwm_freq_hz'], cfg['fan']['min_duty'], cfg['fan']['max_duty']) if cfg['fan']['enabled'] else None

    csv_path = cfg['output']['log_file']
    climate_log = 'logs/climate.csv'
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as f:
            f.write('timestamp,class,confidence,xmin,ymin,xmax,ymax\n')
    if not os.path.exists(climate_log):
        with open(climate_log, 'w') as f:
            f.write('timestamp,temperature,humidity,pressure,fan_duty\n')

    print('Starting Texas Wildlife ID with solar + cellular + motor + climate + fan...')
    last_climate = 0
    try:
        while True:
            if not power.check():
                print('Low battery, skipping frame')
            if climate and fan:
                now = time.time()
                if now - last_climate >= cfg['climate']['log_interval_sec']:
                    data = climate.read()
                    fan.control_by_temp(data.get('temperature'), cfg['fan']['temp_threshold_c'])
                    with open(climate_log, 'a') as f:
                        f.write(f"{datetime.now().isoformat()},{data.get('temperature')},{data.get('humidity')},{data.get('pressure')},{fan.current_duty}\n")
                    last_climate = now

            frame_bgr, img = cam.capture_and_resize(cfg['inference']['input_size'])
            outputs = infer.infer(img)
            boxes = outputs[0][0]
            classes = outputs[1][0].astype(int)
            scores = outputs[2][0]
            h, w = frame_bgr.shape[:2]
            for box, cls, score in zip(boxes, classes, scores):
                if score < cfg['inference']['confidence_threshold']:
                    continue
                ymin, xmin, ymax, xmax = box
                x1 = int(xmin * w); y1 = int(ymin * h); x2 = int(xmax * w); y2 = int(ymax * h)
                label = infer.labels[cls]
                ts = datetime.now().isoformat()
                with open(csv_path, 'a') as f:
                    f.write(f'{ts},{label},{score:.3f},{x1},{y1},{x2},{y2}\n')
                cv2.rectangle(frame_bgr, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame_bgr, f'{label}:{score:.2f}', (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                img_path = None
                if cfg['output']['save_images']:
                    os.makedirs(cfg['output']['save_dir'], exist_ok=True)
                    img_path = os.path.join(cfg['output']['save_dir'], f'{timestamp()}_{label}.jpg')
                    cv2.imwrite(img_path, frame_bgr)
                if motor:
                    motor.trigger(label, cfg['motor']['trigger_on_classes'])
                if cellular and cfg['cellular']['send_on_detection'] and img_path:
                    metadata = f'{ts}|{label}|{score:.3f}'
                    cellular.upload_image(img_path, metadata)
            if cfg['output']['display']:
                cv2.imshow('Texas Wildlife ID', frame_bgr)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
    except KeyboardInterrupt:
        print('Stopping...')
    finally:
        cam.picam2.stop()
        cv2.destroyAllWindows()
        if motor:
            motor.cleanup()
        if fan:
            fan.stop()

if __name__ == '__main__':
    main()
