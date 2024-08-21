import torch
from pytorch3d.renderer import TexturesUV

def resize_texture(texture, target_size):
    _, _, h, w = texture.shape
    if (h, w) != target_size:
        texture = torch.nn.functional.interpolate(texture, size=target_size, mode='bilinear', align_corners=False)
    return texture

def combine_textures(textures):
    combined = None
    for key, texture in textures.items():
        if isinstance(texture, torch.Tensor):
            if combined is None:
                combined = texture.clone()
            else:
                target_size = combined.shape[-2:]
                if texture.shape[-2:] != target_size:
                    texture = resize_texture(texture, target_size)
                if key == 'map_Ka':
                    combined = torch.clamp(combined + texture * 0.2, 0, 1)
                elif key == 'map_Ke':
                    combined = torch.clamp(combined + texture * 0.5, 0, 1)
                elif key == 'map_bump' or key == 'bump':
                    combined = torch.clamp(combined * (1 - texture * 0.2), 0, 1)
    return combined

def apply_textures_to_mesh(mesh, textures, faces_uvs, verts_uvs):
    combined_texture = combine_textures(textures)
    if combined_texture is not None:
        mesh.textures = TexturesUV(maps=combined_texture, faces_uvs=faces_uvs, verts_uvs=verts_uvs)
    else:
        print("No combined texture to apply to the mesh.")
    return mesh
