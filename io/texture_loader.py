import torch
from PIL import Image
import numpy as np
import os

def load_textures_from_mtl(material, texture_dir):
    textures = {}
    for material_name, maps in material.items():
        for map_type, file_name in maps.items():
            if map_type.startswith('map_') or map_type == 'bump':
                map_path = os.path.join(texture_dir, file_name)
                if os.path.exists(map_path):
                    map_image = Image.open(map_path).convert("RGB")
                    textures[map_type] = torch.from_numpy(np.array(map_image)).float() / 255.0
                    textures[map_type] = textures[map_type].permute(2, 0, 1).unsqueeze(0)
                else:
                    print(f"Texture file not found: {map_path}")
            elif map_type == 'color':
                textures['color'] = maps['color']

    return textures
