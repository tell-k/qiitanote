# -*- coding: utf-8 -*-

import os
import time
import subprocess

TARGET_DIR = os.path.join(os.path.dirname(__file__), '..')
cmd = "open --hide -g -a Kobito {}"

# start Koibito.app
subprocess.call(cmd.format(""), shell=True)
time.sleep(3)

# associate .md file to Koibito.app
for root, dirs, files in os.walk(TARGET_DIR):
    for f in files:
        if f.endswith(".md"):
            f = os.path.abspath(os.path.join(root, f))
            subprocess.call(cmd.format(f), shell=True)

# hyde Kobito.app
subprocess.call(
    "osascript -e 'tell application \"Finder\"'"
    " -e 'set visible of process \"Kobito\" to false'"
    " -e 'end tell'",
    shell=True
)
