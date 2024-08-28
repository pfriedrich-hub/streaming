from pathlib import Path
import signal
import sys
import subprocess

JAR_LOCATION = Path.cwd() / 'streaming_noise' / 'game' / 'spaceship.jar'  # TODO based on name and relative path to jar file

# + richtig, - falsch, + Game over, ESC Reset

def main():
    cmd = ['java', '-jar', JAR_LOCATION]
    print(cmd)
    p = subprocess.Popen(cmd)
    try:
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()