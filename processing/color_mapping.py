import numpy as np
from sklearn.neighbors import NearestNeighbors


lego_colors = {
    4: (180, 0, 0),      # Red
    2: (0, 133, 43),     # Green
    1: (30, 90, 168),    # Blue
    14: (250, 200, 10),  # Yellow
    15: (244, 244, 244), # White
    320: (114, 0, 17),   # Dark Red
    36: (201, 26, 9),    # Trans Red
    66: (245, 205, 47),  # Rubber Trans Yellow
    18: (255, 214, 127), # Light Yellow
    216: (135, 43, 23),  # Rust
    7: (138, 146, 141),  # Light Grey
    8: (84, 89, 85),     # Dark Grey
    19: (215, 186, 140), # Tan
    68: (253, 195, 131), # Very Light Orange
    191: (252, 172, 0),  # Bright Light Orange
    366: (216, 109, 44), # Earth Orange
    134: (118, 77, 59),  # Copper
    178: (171, 103, 58), # Pearl Yellow
    300: (194, 127, 83), # Metallic Copper
    10036: (201, 26, 9), # Rubber Trans Red
    10320: (115, 0, 18), # Rubber Dark Red
    176: (148, 81, 72),  # Pearl Red
    508: (255, 128, 20), # Fabuland Red
    484: (145, 80, 28),  # Dark Orange
    422: (145, 92, 60),  # Sienna Brown
    423: (84, 63, 51),   # Umber Brown
    450: (210, 119, 68), # Fabuland Brown
    368: (237, 255, 33), # Neon Yellow
    82: (219, 172, 52),  # Metallic Gold
    334: (194, 152, 46), # Chrome Gold
    0: (27, 42, 52),     # Black
    # More colors can be added if needed
}


def prepare_color_mapping(lego_colors):
    color_values = np.array(list(lego_colors.values()))
    color_ids = list(lego_colors.keys())
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(color_values)
    return nbrs, color_ids

def get_nearest_lego_color(color):
    nbrs, color_ids = prepare_color_mapping(lego_colors)
    color = np.clip(color, 0, 255).astype(int)
    _, indices = nbrs.kneighbors([color])
    nearest_color_id = color_ids[indices[0][0]]
    return nearest_color_id
