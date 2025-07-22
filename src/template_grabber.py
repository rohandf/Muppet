"""
Template Grabber Module

This module:
  - is used for grabbing text templates from text files
  - is used to replace parts of templates before returning them

-RF
"""

import os

# constants, file paths
VMDL_TMP = "../templates/vmdl_template.txt"
MGL_TMP = "../templates/materialgrouplist_template.txt"
MGLR_TMP = "../templates/materialgrouplist_remap_template.txt"
RML_TMP = "../templates/rendermeshlist_template.txt"


# Functions that grab data from templates, then returns it. Some will replace with parameters.
# Raw VMDL Template
def grab_vmdl():  
    with open(
        os.path.join(os.path.dirname(__file__), VMDL_TMP), 'r'
        ) as f_vmdl:
        text = f_vmdl.read()
        return text

# Material Group List
def grab_mgl():
    with open(
        os.path.join(os.path.dirname(__file__), MGL_TMP), 'r'
        ) as f_mgl:
        text = f_mgl.read()
        return text

# Material Group List Remap
def grab_mglr(material_from, material_to):
    with open(
        os.path.join(os.path.dirname(__file__), MGL_TMP), 'r'
        ) as f_mgl:
        text = f_mgl.read()
        text.replace("{REPLACE_TO_ADD_DEFAULT}", material_from)
        text.replace("{REPLACE_TO_ADD_VMAT}", material_to)
        return text

# Render Mesh List
def grab_rml(filename, scale):
    with open(
        os.path.join(os.path.dirname(__file__), RML_TMP), 'r'
        ) as f_rml:
        text = f_rml.read()
        text.replace("{REPLACE_TO_ADD_DMXFBX}", filename)
        text.replace("{REPLACE_TO_ADD_SCALE}", str(scale))
        return text