import os
import yaml
from datetime import datetime

def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def ensure_dirs(config):
    os.makedirs(config['output']['save_dir'], exist_ok=True)
    os.makedirs(os.path.dirname(config['output']['log_file']), exist_ok=True)

def timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
