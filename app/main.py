import subprocess
import sys
import stat
import os
import tempfile
import shutil
import ctypes
UNSHARE = 272
GET_PID = 39
CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL(None)


def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    with tempfile.TemporaryDirectory() as directory_path:
        os.mkdir("{}/tmp".format(directory_path))
        os.mkdir("{}/usr".format(directory_path))
        os.mkdir("{}/usr/local".format(directory_path))
        os.mkdir("{}/usr/local/bin".format(directory_path))
        shutil.copyfile(
            "/usr/local/bin/docker-explorer",
            "{}/usr/local/bin/docker-explorer".format(directory_path),
        )
        os.chroot(directory_path)
        os.chmod(
            "/usr/local/bin/docker-explorer", stat.S_IXGRP | stat.S_IXUSR | stat.S_IXOTH
        )
        libc.syscall(UNSHARE, CLONE_NEWPID)
        process = subprocess.Popen(
            [command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        code = process.wait()
        sys.stdout.write(stdout.decode())
        sys.stderr.write(stderr.decode())
        # os.cloneos.CLONE_NEWPID)
        exit(code)

    completed_process = subprocess.Popen(
        [command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = completed_process.communicate()
    sys.stdout.write(stdout.decode("utf-8"))
    sys.stderr.write(stderr.decode("utf-8"))

    sys.exit(completed_process.returncode)

if __name__ == "__main__":
    main()
