
#!/usr/bin/env python
import argparse
import logging
import os
import re
import shlex
import signal
import sys
import subprocess

log = logging.getLogger(__name__)
SCRIPT = os.path.dirname(os.path.realpath(__file__))
JAR_LOCATION = SCRIPT + "/spaceship.jar"  # TODO based on name and relative path to jar file
DEFAULT_JAVA_OPTS = ""  # TODO fill this with any defaults?

# + richtig, - falsch, + Game over, ESC Reset
g
def arg_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('--java-options', default=DEFAULT_JAVA_OPTS)
    p.add_argument('--jar-path', default=JAR_LOCATION)
    return p


def main(args=None):
    p = arg_parser()
    args, remainder = p.parse_known_args(args)

    java_options = list(DEFAULT_JAVA_OPTS)
    if args.java_options:
        java_options.extend(shlex.split(args.java_options))

    cmd = ['java'] + java_options + remainder + ['-jar', JAR_LOCATION]
    log.critical("Wrapper launching: {}".format(cmd))

    p = subprocess.Popen(cmd)

    try:
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    logging.basicConfig()
    main()