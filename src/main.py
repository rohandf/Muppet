from instance_control import Config, handle_set_command
import os
import re

# VMDL string that will be worked on, saved, and cleared for the next one
vmdl = """"""
# String containing all RenderMeshLists that will be appended to, and placed into vmdl
render_mesh_lists = """"""
# String containing all Material Remaps that will be appende to, and placed into MaterialGroupList
material_group_remaps = """"""
# String containing the MaterialGroupList template, that will have the Remaps inserted into it.
material_group_list = """"""

# this is used to verify if the mod directory is valid. we dont want to ever be writing in diff directories
verify_mod = r"half-life alyx\\content\\hlvr_addons"

while True:
    userinput_contentpath = input("Enter Your Directory: ").strip()
    #userinput_contentpath = r"D:\SteamLibrary\steamapps\common\Half-Life Alyx\content\hlvr_addons\gaming\models\ghostrunner_2\ghostrunner"

    if os.path.exists(userinput_contentpath) and re.search(verify_mod, userinput_contentpath, re.IGNORECASE):
        break

    else:
        print("Path Was Not A Valid Directory\nMust Be In A Addon Folder\n")

# here to load the dmxconvert.exe to pass out later.
verify_dmxconvert = r'dmxconvert.exe'
while True:
    userinput_dmxconvert = input("\nEnter dmxconvert.exe eg:\n" + r"Half-Life Alyx\game\bin\win64\dmxconvert.exe" + "\nEnter : ")
    #userinput_dmxconvert = r"D:\SteamLibrary\steamapps\common\Half-Life Alyx\game\bin\win64\dmxconvert.exe"

    if os.path.isfile(userinput_dmxconvert):
        print("is real exe")
        if re.search(verify_dmxconvert, userinput_dmxconvert, re.IGNORECASE):
            break
        else:
            print("Not A Valid EXE")
    else:
        print("File Does Not Exist")

cfg = Config()

while True:
    command = input(">>> ").strip()
    if not command:
        continue

    tokens = command.split(maxsplit=2)

    if len(tokens) < 3:
        print("Usage: Set <var> <value>")
        continue

    cmd, varname, value = tokens

    if cmd.lower() == "set":
        handle_set_command(cfg, varname, value)

    # Optionally check values after each set
    if cfg.userinput_contentpath:
        if not os.path.exists(cfg.userinput_contentpath) or not re.search(verify_mod, cfg.userinput_contentpath, re.IGNORECASE):
            print("Invalid content path: must exist and be inside an addon folder.")
        else:
            print("Valid content path.")

    if cfg.userinput_dmxconvert:
        if not os.path.isfile(cfg.userinput_dmxconvert):
            print("dmxconvert.exe path is not a valid file.")
        elif not re.search(verify_dmxconvert, cfg.userinput_dmxconvert, re.IGNORECASE):
            print("File is not named dmxconvert.exe.")
        else:
            print("Valid dmxconvert.exe path.")