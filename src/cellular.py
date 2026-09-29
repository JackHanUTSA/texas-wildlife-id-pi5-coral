import requests
import time

class CellularUploader:
    def __init__(self, receiver_url, apn=None, modem_device=None):
        self.receiver_url = receiver_url
        self.apn = apn
        self.modem_device = modem_device
        self.online = True

    def upload_image(self, image_path, metadata):
        if not self.online:
            return False
        try:
            with open(image_path, 'rb') as f:
                files = {'image': (image_path, f, 'image/jpeg')}
                data = {'metadata': metadata}
                resp = requests.post(self.receiver_url, files=files, data=data, timeout=15)
                if resp.status_code == 200:
                    print(f'[CELLULAR] Uploaded {image_path}')
                    return True
                else:
                    print(f'[CELLULAR] Upload failed {resp.status_code}')
                    return False
        except Exception as e:
            print(f'[CELLULAR] Error {e}')
            return False

    def check_link(self):
        return self.online
