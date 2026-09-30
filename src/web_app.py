from flask import Flask, jsonify, request, send_from_directory
import yaml
import os

app = Flask(__name__, static_folder='../web/static')

CONFIG_PATH = 'config.yaml'
LOG_PATH = 'logs/detections.csv'
CLIMATE_LOG = 'logs/climate.csv'

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status')
def status():
    cfg = load_config()
    last_detection = None
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            lines = f.readlines()
            if len(lines) > 1:
                last_detection = lines[-1].strip().split(',')
    climate = None
    if os.path.exists(CLIMATE_LOG):
        with open(CLIMATE_LOG) as f:
            lines = f.readlines()
            if len(lines) > 1:
                parts = lines[-1].strip().split(',')
                climate = {
                    'timestamp': parts[0],
                    'temperature': parts[1],
                    'humidity': parts[2],
                    'pressure': parts[3],
                    'fan_duty': parts[4]
                }
    return jsonify({'config': cfg, 'last_detection': last_detection, 'climate': climate})

@app.route('/api/control', methods=['POST'])
def control():
    data = request.json
    action = data.get('action')
    return jsonify({'result': 'ok', 'action': action})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
