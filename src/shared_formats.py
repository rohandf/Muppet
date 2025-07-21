'''
Shared Formats Module

This module:
    the name is rather misleading. this module is used for FILE HANDLING
    Finding, Reading, Extracting, ect this is all done within this Python Module

    Special use cases it can extract from FBXs and DMXs
    * Extract Materials From DMX/FBX
    * Extract Bones From DMX/FBX

-DOURAN
'''

import os
import subprocess # this is used to run dmxconvert
import fbx
import fbx_common 
import re

OUT_DMX = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dmx_data"))

# is this a overkill setup to reduce the count of if statements to 2. yes- yes it is
# THIS IS NOT USED IN MAIN BUT USED IN find_files
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

def find_files(input, extensions, verify=False):
    matches = []
    extensions = [ext.lower() for ext in extensions]

    for dirpath, _, filenames in os.walk(input):
        for file in filenames:
            if any(file.lower().endswith(ext) for ext in extensions):
                full_path = os.path.join(dirpath, file)
                if verify:
                    if verify_files(full_path):
                        matches.append(full_path)
                else:
                    matches.append(full_path)
    return matches

# strips file paths to filenames and adds them to a list 
def strip_to_filenames(paths, rm_ext=False):
    if rm_ext:
        return [os.path.splitext(os.path.basename(path))[0] for path in paths]
    else:
        return [os.path.basename(path) for path in paths]

def run_dmxconvert(userdmx, passdmx, passoutputfile):
    output_path = OUT_DMX + passoutputfile

    args = [
        userdmx,
        "-i", passdmx,
        "-ie", "binary",
        "-o", output_path,
        "-of", "vtex"
    ]

    print("Running:", args)
    dmxconvert = subprocess.run(args, capture_output=True, text=True)
    print(dmxconvert.stdout)
    print(dmxconvert.stderr)

dmx_material_pattern = r'"material"\s+"DmeMaterial"\s*\{[^}]*?"name"\s+"string"\s+"([^"]+)"'
def extract_dmx_materials(input):
    with open(input, "r", encoding="utf-8", errors="ignore") as dmx:
        matches = re.findall(dmx_material_pattern, dmx.read())
        return matches if matches else False
    
dmx_bones_pattern = r'"DmeTransform"\s*\{[^}]*?"name"\s+"string"\s+"([^"]+)"'
def extract_dmx_bones(input):
    with open(input, "r", encoding="utf-8", errors="ignore") as dmx:
        bones = re.findall(dmx_bones_pattern, dmx.read())
        return bones if bones else False

def extract_fbx_materials(input):
    # Create the FBX SDK manager and scene
    manager, scene = fbx_common.InitializeSdkObjects()
    
    # Load the FBX file
    result = fbx_common.LoadScene(manager, scene, input)
    if not result:
        print("Failed to load FBX file.")
        return []

    material_names = set()

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

def extract_fbx_bones(input):
    manager, scene = fbx_common.InitializeSdkObjects()
    if not fbx_common.LoadScene(manager, scene, input):
        return []

    bone_names = []

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