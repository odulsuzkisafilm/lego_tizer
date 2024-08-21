from pytorch3d.io import load_objs_as_meshes

def load_obj_mesh(obj_path):
    return load_objs_as_meshes([obj_path])
