import subprocess
import sys
import stat
import os
import tempfile
import shutil


def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    directory_path = tempfile.mkdtemp()
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

    completed_process = subprocess.Popen(
        [command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = completed_process.communicate()
    sys.stdout.write(stdout.decode("utf-8"))
    sys.stderr.write(stderr.decode("utf-8"))

    sys.exit(completed_process.returncode)

if __name__ == "__main__":
    main()
