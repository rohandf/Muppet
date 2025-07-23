from template_grabber import grab_rml
from shared_formats import find_files

def rml_operations(input, scale=float(1)):
    render_mesh_lists = []

    real_mesh = f'"{input}"'
    rendermeshlist_append = grab_rml(real_mesh, scale)
    render_mesh_lists.append(rendermeshlist_append)

    return render_mesh_lists