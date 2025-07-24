'''
Shared Formats Module

This module:
    the name is rather misleading. this module is used for FILE HANDLING
    Finding, Reading, Extracting, ect this is all done within this Python Module

    ## Special use cases it can extract from FBXs and DMXs
    * Extract Materials From DMX/FBX
    * Extract Bones From DMX/FBX

-DOURAN
'''

import os
import subprocess # this is used to run dmxconvert
import fbx
import fbx_common # this is used to cut down the amount of code for fbxs.
import re


OUT_DMX = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dmx_data")) # OUT_DMX = ~\dmx_data. 
# this checks where dmx_data is compared to the python file. its always one level up

# is this a overkill setup to reduce the count of if statements to 2. yes- yes it is
# verify_files IS NOT USED IN MAIN BUT USED IN find_files

# checks the header of a file to look for a match.
# the matches are just a basic string that contains basic header line that are found in these file types
# dmx checks if its a binary 9 model 22 format. fbx just checks for the generic fbx header
# it is case senstive
# if match return True. else Return False
def verify_files(input):
    validators = {
        ".dmx": ("Not A Valid DMX", r"<!-- dmx encoding binary 9 format model 22 -->"),
        ".fbx": ("Not A Valid FBX", r"Kaydara FBX Binary")
    }

    for ext, (error_msg, pattern) in validators.items():
        if input.lower().endswith(ext):
            with open(input, "r", encoding="utf-8", errors="ignore") as f:
                if re.search(pattern, f.read()):
                    return True
                else:
                    print(f"{input} {error_msg}")
                    return False
    return False

# it does not scan recursively into directories. if u wish to do that pair this up with descend_into_dir
def find_files(input, ends_with=None, verify=False): 
    # seens is used to track for dupes. is this redunant. probably
    seen = set()
    ends_with = [ext.lower() for ext in (ends_with or [])]

    return [
        # iterate over each item in the directory, joined to the full path
        f for f in (os.path.join(input, name) for name in os.listdir(input))
        # only include files (not directories)
        if os.path.isfile(f)
        # if ends_with is provided, check if file ends with one of the extensions
        and (not ends_with or any(f.lower().endswith(ext) for ext in ends_with))
        # skip files already seen (normalized, lowercase path)
        and not (os.path.normpath(f).lower() in seen or seen.add(os.path.normpath(f).lower()))
        # if verify is true, only include files that pass the verify_files function
        and (not verify or verify_files(f))
    ]

# strips file paths to filenames and adds them to a list. rm_ext = remove extensions from paths
def strip_to_filenames(paths, rm_ext=False):
    if rm_ext:
        return [os.path.splitext(os.path.basename(path))[0] for path in paths]
    else:
        return [os.path.basename(path) for path in paths]

# some bullshit
def descend_into_dir(input, limit=9999, stop_if="", look_for="", hide_if="", case_sensitive=True, only_look_for=False):
    def match_check(haystack, needle):
        if not case_sensitive:
            haystack = haystack.lower()
            needle = needle.lower()
        if only_look_for:
            # Check if the full path ends with the needle
            return haystack.endswith(needle)
        else:
            return needle in haystack

    count = 0
    seen = set()  # Track yielded directories

    for root, dirs, _ in os.walk(input):
        for d in dirs:
            full_path = os.path.normcase(os.path.join(root, d))  # Normalize case here

            if full_path in seen:
                continue  # Skip duplicates

            # Stop early
            if stop_if and match_check(full_path, stop_if):
                return

            # Skip hidden
            if hide_if and match_check(full_path, hide_if):
                continue

            # Check look_for
            if look_for:
                if match_check(full_path, look_for):
                    seen.add(full_path)
                    yield full_path
                    count += 1
            else:
                seen.add(full_path)
                yield full_path
                count += 1

            if count >= limit:
                return

def ascend_dir(input, limit=9999, stop_if="", look_for="", hide_if="", case_sensitive=True, only_look_for=False):
    def match_check(haystack, needle):
        if not case_sensitive:
            haystack = haystack.lower()
            needle = needle.lower()
        if only_look_for:
            # Check if the full path ends with the needle
            return haystack.endswith(needle)
        else:
            return needle in haystack

    count = 0
    current = os.path.abspath(input)

    while True:
        if hide_if and match_check(current, hide_if):
            #print(f"[-] Skipping hidden: '{current}'")
            pass
        elif stop_if and match_check(current, stop_if):
            #print(f"[!] Stopping early: '{stop_if}' found in '{current}'")
            return
        elif not look_for or match_check(current, look_for):
            yield current
            count += 1

        if count >= limit:
            #print(f"[!] Limit of {limit} reached. Stopping.")
            return

        parent = os.path.dirname(current)
        if parent == current:
            # reached root
            return
        current = parent

def run_dmxconvert(userdmx, passdmx, passoutputfile):

    # userdmx = dmxconvert.exe, passdmx is the dmx file, passouputfile is the output
    # arguments for running dmx convert
    args = [
        userdmx,
        "-i", passdmx,
        "-ie", "binary",
        "-o", passoutputfile,
        "-of", "vtex"
    ]

    print("Running:", args)
    #triggers dmxconvert. capture ouput later for text. text=true displays text from output
    dmxconvert = subprocess.run(args, capture_output=True, text=True)
    print(dmxconvert.stdout)
    print(dmxconvert.stderr)

dmx_material_pattern = r'"material"\s+"DmeMaterial"\s*\{[^}]*?"name"\s+"string"\s+"([^"]+)"'
def extract_dmx_materials(input):
    with open(input, "r", encoding="utf-8", errors="ignore") as dmx:
        matches = re.findall(dmx_material_pattern, dmx.read())
        #return matches if matches else False
        return matches if matches else []

dmx_bones_pattern = r'"DmeTransform"\s*\{[^}]*?"name"\s+"string"\s+"([^"]+)"'
def extract_dmx_bones(input):
    with open(input, "r", encoding="utf-8", errors="ignore") as dmx:
        bones = re.findall(dmx_bones_pattern, dmx.read())
        #return bones if bones else False
        return bones if bones else []

#adds in a list
def extract_fbx_materials(input):
    # Create the FBX SDK manager and scene
    manager, scene = fbx_common.InitializeSdkObjects()
    
    # Load the FBX file
    result = fbx_common.LoadScene(manager, scene, input)
    if not result:
        print("Failed to load FBX file.")
        return []

    material_names = set()

    # nodes are vars that store a certain data type. in here we are trying to get a node of the type material.
    def traverse_node(node):
        # Check materials assigned to this node
        material_count = node.GetMaterialCount()
        for i in range(material_count):
            material = node.GetMaterial(i)
            if material:
                name = material.GetName()
                if name:
                    material_names.add(name)
        
        # Recurse through child nodes
        for i in range(node.GetChildCount()):
            traverse_node(node.GetChild(i))

    root_node = scene.GetRootNode()
    if root_node:
        traverse_node(root_node)

    return list(material_names)

#adds in a array. why is it diff above. i have no idea
def extract_fbx_bones(input):
    manager, scene = fbx_common.InitializeSdkObjects()
    if not fbx_common.LoadScene(manager, scene, input):
        return []

    bone_names = []

    # nodes are vars that store a certain data type. in here we are trying to get a node of the type material.
    def traverse(node):
        attr = node.GetNodeAttribute()
        if attr and attr.GetAttributeType() == fbx.FbxNodeAttribute.EType.eSkeleton:
            bone_names.append(node.GetName())
        for i in range(node.GetChildCount()):
            traverse(node.GetChild(i))

    root = scene.GetRootNode()
    if root:
        traverse(root)

    return bone_names