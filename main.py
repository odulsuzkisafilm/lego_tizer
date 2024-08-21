import sys
from lego_tizer import load_obj_mesh
from lego_tizer import parse_mtl
from lego_tizer import load_textures_from_mtl
from lego_tizer import write_ldr_with_texmap, parse_ldr_file, write_improved_ldr_file, write_grouped_ldr_file
from lego_tizer import lego_tize, inspect_vertex_distribution
from lego_tizer import apply_textures_to_mesh
from lego_tizer import find_neighbors, group_bricks, replace_with_larger_bricks


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python main.py <obj_path> <mtl_path> <texture_dir> [<output_path>]")
        sys.exit(1)

    # Parse command-line arguments for the paths
    obj_path = sys.argv[1]
    mtl_path = sys.argv[2]
    texture_dir = sys.argv[3]

    # Set the output path; default to 'output.ldr' if not provided
    if len(sys.argv) == 5:
        output_path = sys.argv[4]
    else:
        output_path = "output.ldr"

    # Parse the MTL file to extract material properties and texture information
    material = parse_mtl(mtl_path)
    # Load textures based on the material properties from the MTL file
    textures = load_textures_from_mtl(material, texture_dir)

    # Load the 3D mesh from the OBJ file
    mesh = load_obj_mesh(obj_path)
    # Inspect the vertex distribution before any processing
    inspect_vertex_distribution(mesh)

    # Scale the vertices of the mesh for LEGO-tizing, multiplying by 1000 for better precision
    vertices = mesh.verts_packed() * 1000.0
    mesh = mesh.update_padded(new_verts_padded=vertices.unsqueeze(0))
    # Inspect the vertex distribution after scaling
    inspect_vertex_distribution(mesh)

    # Extract UV coordinates from the mesh for texture mapping
    verts_uvs = mesh.textures.verts_uvs_padded()[0]
    faces_uvs = mesh.textures.faces_uvs_padded()[0]
    verts_uvs = verts_uvs.unsqueeze(0)  # Adjust the dimensions for compatibility
    faces_uvs = faces_uvs.unsqueeze(0)

    # Apply the combined textures to the mesh
    mesh = apply_textures_to_mesh(mesh, textures, faces_uvs, verts_uvs)
    # LEGO-tize the mesh by rounding vertices to align with LEGO brick grid
    lego_mesh = lego_tize(mesh)

    # Write the initial LDR file with the LEGO-tized mesh and applied textures
    write_ldr_with_texmap(lego_mesh, output_path, textures, material.get('color', None))

    # Parse the generated LDR file to extract brick information
    bricks = parse_ldr_file(output_path)
    # Find and add neighboring bricks to fill in gaps and enhance the model
    bricks_with_neighbors = find_neighbors(bricks)

    # Write the improved LDR file with added neighboring bricks
    write_improved_ldr_file(output_path, bricks_with_neighbors)

    # Group bricks based on proximity and replace small bricks with larger ones if possible
    grouped_bricks = group_bricks(bricks_with_neighbors)
    replaced_bricks = replace_with_larger_bricks(grouped_bricks)

    # Write the final grouped LDR file with optimized brick placement
    write_grouped_ldr_file(output_path, replaced_bricks)


if __name__ == "__main__":
    main()
