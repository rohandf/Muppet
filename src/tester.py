import material_operations
import shared_formats
from rapidfuzz import process, fuzz
import pprint


test_dir = r"D:\VSC projects\PRS2Tool\test"
files = shared_formats.find_files(test_dir, [".dmx",".fbx"], verify=True)

def make_remap_dict():
    for file in files:
        materials = shared_formats.extract_fbx_materials(file)
        mat_dict = {} #dict of material from-to pairs
        for material in materials:
            choices = ["pants_mat.vmat", "Pnats_Mat.vmat", "Pants_Mat.vmat", "Props_mat.vmat"]
            #use process.extractone with fuzz.ratio, compare matname to looped-over all vmats
            result = process.extractOne(material, choices, scorer=fuzz.ratio, score_cutoff=60)
            # if no valid matches
            if result != None:
                mat_dict[material] = result[0]
                print(result[1])
            else:
                pass
                #mat_dict[material] = material+".vmat"

        return mat_dict
    