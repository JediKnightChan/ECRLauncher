import os
import yadisk
import logging

logger = logging.getLogger('multiprocess-queue-logger')


class YandexDriveWorker:
    def __init__(self, app_id, app_key, app_token):
        self.disk = yadisk.YaDisk(app_id, app_key, app_token)

    def download_file(self, local_filepath, ydrive_public_key):
        if os.path.dirname(local_filepath):
            os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
        self.disk.download_public(ydrive_public_key, local_filepath)


if __name__ == '__main__':
    app_id = "f655b1c4fb2d45ebb46bb0156321e211"
    app_key = "188834c6ed004363a2b1634b4534a20a"
    app_token = ""
    yw = YandexDriveWorker(app_id, app_key, app_token)
    yw.download_file("ecr.jpg", "some path id")
