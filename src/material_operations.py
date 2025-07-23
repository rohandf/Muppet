"""
This module is responsible for constructing the list of material classes,
to be later grabbed into the function that constructs the final vmdl.

-RF
"""

import template_grabber as tg
import shared_formats
from rapidfuzz import process, fuzz


# accepts dictionary of from-to materials
def add_mats(mat_dict) -> str:
    remaps = ""
    for from_mat, to_mat in mat_dict.items():
        tmp_remap = tg.grab_mglr(from_mat, to_mat)
        remaps = remaps + tmp_remap
    return(make_mat_class(remaps))

# places all remaps into materialgrouplist class, called automatically after add_mats
def make_mat_class(remaps) -> str:
    final_mgl = tg.grab_mgl()
    final_mgl = final_mgl.replace("{REPLACE_TO_ADD_REMAPS}", remaps)
    return final_mgl

#constructs dictionary to create remaps from from-to pairs
def make_remap_dict(f_mats,t_mats) -> dict:
    mat_dict = {} #dict of material from-to pairs
    for f_mat in f_mats:
        #use process.extractone with fuzz.ratio, compare matname to looped-over all vmats (t_mats, target vmats)
        result = process.extractOne(f_mat, t_mats, scorer=fuzz.ratio, score_cutoff=60)
        if result != None:
            mat_dict[f_mat] = result[0]
            print(result[1])
        else: # if no valid matches:
            pass # do nothing
    add_mats(mat_dict)

# call this to start the chain. returns a MaterialGroupList class.
def get_mats_from_dir(md_dir, vmat_dir) -> str:
    files = shared_formats.find_files(md_dir, [".dmx",".fbx"], verify=True)
    f_mats = []
    for file in files:
        f_mats = shared_formats.extract_fbx_materials(file)
    t_mats = shared_formats.find_files(vmat_dir, [".vmat"])
    return(make_remap_dict(f_mats,t_mats)) 