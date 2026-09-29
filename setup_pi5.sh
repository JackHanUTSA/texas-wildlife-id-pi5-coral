#!/bin/bash
set -e
sudo apt update
sudo apt install -y python3-pip libatlas-base-dev
pip3 install -r requirements.txt
# Install Edge TPU runtime
echo "Install Edge TPU runtime from https://coral.ai/docs/accelerator/get-started/"
# Enable camera
sudo raspi-config nonint do_camera 0
echo "Setup complete. Copy models/ to Pi."
