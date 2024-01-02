import subprocess
import sys


def main():
    # print("Logs from your program will appear here!")
    command = sys.argv[3]
    args = sys.argv[4:]

    completed_process = subprocess.Popen(
        [command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = completed_process.communicate()
    sys.stdout.write(stdout.decode("utf-8"))
    sys.stderr.write(stderr.decode("utf-8"))


if __name__ == "__main__":
    main()
