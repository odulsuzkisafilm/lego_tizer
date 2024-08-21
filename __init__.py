from .io.obj_loader import load_obj_mesh
from .io.mtl_parser import parse_mtl
from .io.texture_loader import load_textures_from_mtl
from .io.ldr_writer import write_ldr_with_texmap, parse_ldr_file, write_improved_ldr_file, write_grouped_ldr_file

from .processing.color_mapping import lego_colors, get_nearest_lego_color, prepare_color_mapping
from .processing.mesh_operations import lego_tize, inspect_vertex_distribution
from .processing.texture_operations import apply_textures_to_mesh, combine_textures, resize_texture
from .processing.brick_operations import find_neighbors, group_bricks, replace_with_larger_bricks

from .utils.debug import debug_texture_application
