from .color_mapping import lego_colors, get_nearest_lego_color, prepare_color_mapping
from .mesh_operations import lego_tize, inspect_vertex_distribution
from .texture_operations import apply_textures_to_mesh, combine_textures, resize_texture
from .brick_operations import find_neighbors, group_bricks, replace_with_larger_bricks

__all__ = [
    "lego_colors",
    "get_nearest_lego_color",
    "prepare_color_mapping",
    "lego_tize",
    "inspect_vertex_distribution",
    "apply_textures_to_mesh",
    "combine_textures",
    "find_neighbors",
    "group_bricks",
    "replace_with_larger_bricks",
    "resize_texture"
]
