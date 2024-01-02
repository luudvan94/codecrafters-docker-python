from io import FileIO
import subprocess
import sys
import stat
import os
import tempfile
import shutil
import ctypes
import urllib.request
import json
import tarfile

UNSHARE = 272
GET_PID = 39
CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL(None)

def get_token(image):
    url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/{image}:pull"
    return json.loads(urllib.request.urlopen(url).read())["token"]

def main():
    image_info = sys.argv[2]
    if ":" not in image_info:
        image_info += ":latest"
    image, version = image_info.split(":")
    token = get_token(image)
    manifest_url = (
        f"https://registry.hub.docker.com/v2/library/{image}/manifests/{version}"
    )
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": "Bearer " + token,
    }
    req = urllib.request.Request(manifest_url, headers=headers)
    manifest = json.loads(urllib.request.urlopen(req).read())
    command = sys.argv[3]
    args = sys.argv[4:]

    with tempfile.TemporaryDirectory() as directory_path:
        # os.mkdir("{}/tmp".format(directory_path))
        # os.mkdir("{}/usr".format(directory_path))
        # os.mkdir("{}/usr/local".format(directory_path))
        # os.mkdir("{}/usr/local/bin".format(directory_path))
        for layer in manifest["layers"]:
            digest = layer["digest"]
            layer_url = (
                f"https://registry.hub.docker.com/v2/library/{image}/blobs/{digest}"
            )
            header = {"Authorization": "Bearer " + token}
            req = urllib.request.Request(layer_url, headers=header)
            response = urllib.request.urlopen(req)
            tar_filename = f"/tmp/ff.tar.gz"
            new_tar = open(tar_filename.format(digest), "wb")
            new_tar.write(response.read())
            tar = tarfile.open(tar_filename)
            tar.extractall(directory_path)
            tar.close()
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
