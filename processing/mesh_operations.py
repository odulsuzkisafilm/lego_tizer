import torch

def lego_tize(mesh, grid_size=(20, 24, 20), scale_factor=1000.0):
    vertices = mesh.verts_packed() * scale_factor
    lego_vertices_x = torch.round(vertices[:, 0] / grid_size[0]) * grid_size[0]
    lego_vertices_y = torch.round(vertices[:, 1] / grid_size[1]) * grid_size[1]
    lego_vertices_z = torch.round(vertices[:, 2] / grid_size[2]) * grid_size[2]
    lego_vertices = torch.stack([lego_vertices_x, lego_vertices_y, lego_vertices_z], dim=1)
    mesh._verts_list = [lego_vertices]
    return mesh

def inspect_vertex_distribution(mesh):
    vertices = mesh.verts_packed()
    print("Original Vertex Positions:")
    print(vertices)
