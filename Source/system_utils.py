import ctypes
import sys


def is_windows_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def rerun_as_windows_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)