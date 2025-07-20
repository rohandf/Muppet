import os
import re

# this is used to verify if the mod directory is valid. we dont want to ever be writing in diff directories

verify_mod = r"half-life alyx\\content\\hlvr_addons"

while True:
    userinput_contentpath = input("Enter Your Addon Directory: ").strip()

    if os.path.exists(userinput_contentpath) and re.search(verify_mod, userinput_contentpath, re.IGNORECASE):
        print(":)")
        break

    else:
        print("Path Was Not A Valid Mod Directory\n")