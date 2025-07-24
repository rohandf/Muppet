import material_operations
import os
import shared_formats

mesh_dir = "D:/VSC projects/PRS2Tool/test/doom_dark_ages/characters/heros/slayer/Source/Slayer_UpperBody.txt"
vmat_dir = "D:/VSC projects/PRS2Tool/test/doom_dark_ages/characters/heros/slayer/Materials/Textures"
vmat_list = []

vmat_dir = os.listdir(vmat_dir)
for vmat in vmat_dir:
    if vmat.endswith(".vmat"):
        vmat_list.append(vmat)

#print(vmat_list)

print(material_operations.get_mats_from_dir(mesh_dir, vmat_list))

#print(shared_formats.extract_dmx_materials(mesh_dir))