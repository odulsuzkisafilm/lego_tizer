import numpy as np
from lego_tizer import get_nearest_lego_color, resize_texture


# Extract colors and map them using all maps combined
def write_ldr_with_texmap(mesh, output_path, textures, material_color=None, brick_size=(20, 24, 20)):
    verts = mesh.verts_packed()
    faces = mesh.faces_packed()

    bx, by, bz = brick_size

    if 'map_Kd' in textures:
        diffuse_map = textures['map_Kd'].squeeze(0).permute(1, 2, 0) * 255  # Get the diffuse texture
        target_size = (diffuse_map.shape[0], diffuse_map.shape[1])

        for key in ['map_Ka', 'map_Ke', 'bump']:
            if key in textures:
                textures[key] = resize_texture(textures[key], target_size)

        verts_uvs = mesh.textures.verts_uvs_padded()[0]
        texture_h, texture_w, _ = diffuse_map.shape

        colors = [15] * verts.shape[0]

        for i, uv in enumerate(verts_uvs):
            u, v = uv.numpy()
            x = int(np.clip(u * texture_w, 0, texture_w - 1))
            y = int(np.clip((1 - v) * texture_h, 0, texture_h - 1))

            combined_color = diffuse_map[y, x].numpy()

            if 'map_Ka' in textures:
                ambient_color = textures['map_Ka'].squeeze(0).permute(1, 2, 0)[y, x].numpy() * 255 * 0.2
                combined_color = np.clip(combined_color + ambient_color, 0, 255)
            if 'map_Ke' in textures:
                emission_color = textures['map_Ke'].squeeze(0).permute(1, 2, 0)[y, x].numpy() * 255 * 0.5
                combined_color = np.clip(combined_color + emission_color, 0, 255)
            if 'bump' in textures:
                bump_intensity = textures['bump'].squeeze(0).permute(1, 2, 0)[y, x].mean().numpy()
                combined_color = np.clip(combined_color * (1 - bump_intensity * 0.2), 0, 255)

            lego_color_id = get_nearest_lego_color(combined_color)
            colors[i] = lego_color_id

        assert len(colors) == verts.shape[0], "Mismatch between number of vertices and colors."
    elif material_color:
        colors = [get_nearest_lego_color(material_color)] * verts.shape[0]
    else:
        colors = [15] * verts.shape[0]

    with open(output_path, "w") as f:
        f.write("0 LEGO-tized Model\n")

        placed_bricks = set()  # To track placed brick positions

        for vert, color in zip(verts, colors):
            x, y, z = vert.tolist()

            # Applying a small offset to avoid collapsing to the same position
            x = round((x + 0.1) / bx) * bx
            y = round((y + 0.1) / by) * by
            z = round((z + 0.1) / bz) * bz

            # Checking if the brick position has already been used
            if (x, y, z) not in placed_bricks:
                placed_bricks.add((x, y, z))
                f.write(f"1 {color} {int(x)} {-int(y)} {int(z)} 1 0 0 0 1 0 0 0 1 3005.DAT\n")


def parse_ldr_file(ldr_path):
    bricks = []
    with open(ldr_path, 'r') as file:
        for line in file:
            if line.startswith("1"):  # Brick placement line
                parts = line.split()
                color_id = int(parts[1])
                x, y, z = int(parts[2]), int(parts[3]), int(parts[4])
                bricks.append((color_id, x, y, z))
    return bricks


def write_improved_ldr_file(ldr_path, bricks):
    with open(ldr_path, 'w') as file:
        file.write("0 Improved LEGO Model\n")
        for color_id, x, y, z in bricks:
            file.write(f"1 {color_id} {x} {y} {z} 1 0 0 0 1 0 0 0 1 3005.DAT\n")


def write_grouped_ldr_file(ldr_path, bricks):
    with open(ldr_path, 'w') as file:
        file.write("0 Grouped LEGO Model\n")
        for brick in bricks:
            if len(brick) == 4:
                color_id, x, y, z = brick[:4]
                file.write(f"1 {color_id} {x} {y} {z} 1 0 0 0 1 0 0 0 1 3005.DAT\n")
            elif len(brick) == 5:
                color_id, x, y, z, part = brick
                file.write(f"1 {color_id} {x} {y} {z} 1 0 0 0 1 0 0 0 1 {part}\n")
