import subprocess
import tempfile
import sys
import os
import shutil


def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    dirpath = tempfile.mkdtemp()
    shutil.copy2(command, dirpath)
    os.chroot(dirpath)
    new_command = "/" + os.path.basename(command)
    

    completed_process = subprocess.Popen(
        [new_command, *args], capture_output=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = completed_process.communicate()
    sys.stdout.write(stdout.decode("utf-8"))
    sys.stderr.write(stderr.decode("utf-8"))

    sys.exit(completed_process.returncode)

if __name__ == "__main__":
    main()
