import shlex
import os
import subprocess
from logging import log


def run_detached_process(cmd, logging_file="log.txt", do_print_logging=False):
    cmds = shlex.split(cmd)
    if os.name == "posix":
        # Linux
        subprocess.Popen(cmds, start_new_session=True)
    elif os.name == "nt":
        # Windows
        flags = 0
        flags |= 0x00000008  # DETACHED_PROCESS
        flags |= 0x00000200  # CREATE_NEW_PROCESS_GROUP
        flags |= 0x08000000  # CREATE_NO_WINDOW

        pkwargs = {
            'close_fds': True,  # close stdin/stdout/stderr on child
            'creationflags': flags,
        }
        subprocess.Popen(cmds, **pkwargs)
    else:
        log("Unknown os" + os.name, logging_file, do_print_logging)
