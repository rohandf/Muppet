import os
import subprocess #this is used for run dmxconvert
import fbx
import re #this is used to read the dmx

verify_dmx = r"<!-- dmx encoding binary 9 format model 22 -->"
verify_fbx = r"Kaydara FBX Binary"

def verify_files(usermod):
    if usermod.lower().endswith(".fbx"):
        with open(usermod, "r", encoding="utf-8", errors="ignore") as fbx:
            if re.search(verify_fbx, fbx.read()):
                print("is real fbx")
            else:
                print("Not A Valid FBX")
                return
    
    if usermod.lower().endswith(".dmx"):
        with open(usermod, "r", encoding="utf-8", errors="ignore") as dmx:
            if re.search(verify_dmx, dmx.read()):
                print("is real dmx")
            else:
                print("Not A Valid DMX")
                print("Must Be Binary 9 Format Model 22")
                return

def handle_files(usermod):
    try:
        pass
    
    except Exception as e:
        print(f"{e}")

def run_dmxconvert():
    pass