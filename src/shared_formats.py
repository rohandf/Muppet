import os
import subprocess #this is used to run dmxconvert
import fbx
import re

verify_dmx = r"<!-- dmx encoding binary 9 format model 22 -->"
verify_fbx = r"Kaydara FBX Binary"

def verify_files(usermod):
    validators = {
        ".fbx": ("is real fbx", "Not A Valid FBX", verify_fbx),
        ".dmx": ("is real dmx", "Not A Valid DMX", verify_dmx)
    }

    for ext, (true_msg, error_msg, pattern) in validators.items():
        if usermod.lower().endswith(ext):
            with open(usermod, "r", encoding="utf-8", errors="ignore") as f:
                if re.search(pattern, f.read()):
                    print(true_msg)
                else:
                    print(error_msg)

def handle_files(usermod):
    try:
        pass
    
    except Exception as e:
        print(f"{e}")

def run_dmxconvert():
    pass