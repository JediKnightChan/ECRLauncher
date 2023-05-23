import os
import time
import zipfile

from ecr_logging import log
from detached_process_launcher import run_detached_process
from system_utils import rerun_as_windows_admin, is_windows_admin

if __name__ == '__main__':
    log_dst = "launcher_update_log.txt"
    do_print = True

    if os.name == "nt":
        # Require admin rights
        if not is_windows_admin():
            rerun_as_windows_admin()

    log("Launcher update queued...", filename=log_dst, do_print=do_print)

    time.sleep(3)

    log("Updating launcher", filename=log_dst, do_print=do_print)

    zip_destination = "launcher.zip"

    try:
        with zipfile.ZipFile(zip_destination, 'r') as zip_ref:
            zip_ref.extractall(".")

        log("Launcher updated successfully", filename=log_dst, do_print=do_print)

        os.remove(zip_destination)

        if os.name == "nt":
            # Windows
            cmd = "launcher.exe"
        else:
            cmd = None

        if cmd and not os.path.exists(cmd):
            cmd = None

        if os.path.exists(cmd):
            run_detached_process(cmd, log_dst, do_print)

    except Exception as e:
        log("Error occurred while installing launcher update", filename=log_dst, do_print=do_print)
        log(e, filename=log_dst, do_print=do_print)
