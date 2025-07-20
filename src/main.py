
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
    userinput_contentpath = input("Enter Your Addon Directory: ").strip()

    if os.path.exists(userinput_contentpath) and re.search(verify_mod, userinput_contentpath, re.IGNORECASE):
        print(":)")
        break

    else:
        print("Path Was Not A Valid Mod Directory\n")