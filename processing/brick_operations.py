def find_neighbors(bricks, grid_size=(20, 24, 20)):
    x_step, y_step, z_step = grid_size
    directions = [
        (x_step, 0, 0), (-x_step, 0, 0),  # x-axis neighbors
        (0, y_step, 0), (0, -y_step, 0),  # y-axis neighbors
        (0, 0, z_step), (0, 0, -z_step)   # z-axis neighbors
    ]

    brick_set = set((x, y, z) for _, x, y, z in bricks)
    new_bricks = []

    for color_id, x, y, z in bricks:
        for dx, dy, dz in directions:
            neighbor_pos = (x + dx, y + dy, z + dz)
            if neighbor_pos not in brick_set:
                # Add a brick in the empty position
                new_bricks.append((color_id, *neighbor_pos))
                brick_set.add(neighbor_pos)  # Mark as occupied

    return bricks + new_bricks


def group_bricks(bricks, grid_size=(20, 24, 20)):
    x_step, y_step, z_step = grid_size
    directions = [
        (x_step, 0, 0),  # x-axis
        (0, y_step, 0),  # y-axis
        (0, 0, z_step)   # z-axis
    ]

    grouped_bricks = []
    visited = set()

    for i, (color_id, x, y, z) in enumerate(bricks):
        if (x, y, z) in visited:
            continue

        # Start a new group
        group = [(color_id, x, y, z)]
        visited.add((x, y, z))

        for dx, dy, dz in directions:
            next_x, next_y, next_z = x + dx, y + dy, z + dz
            if (color_id, next_x, next_y, next_z) in bricks:
                if (next_x, next_y, next_z) not in visited:
                    group.append((color_id, next_x, next_y, next_z))
                    visited.add((next_x, next_y, next_z))

        grouped_bricks.append(group)

    return grouped_bricks


def replace_with_larger_bricks(grouped_bricks):
    replaced_bricks = []

    for group in grouped_bricks:
        if len(group) == 1:
            # No grouping needed, keep as 1x1 brick
            replaced_bricks.extend(group)
        elif len(group) == 2:
            # Replace with a 1x2 brick (3004.DAT)
            color_id, x, y, z = group[0]
            if group[1][1] == x + 20:  # If next brick is to the right
                replaced_bricks.append((color_id, x, y, z, "3004.DAT"))
            elif group[1][2] == y + 24:  # If next brick is above
                replaced_bricks.append((color_id, x, y, z, "3004.DAT"))
            elif group[1][3] == z + 20:  # If next brick is in front
                replaced_bricks.append((color_id, x, y, z, "3004.DAT"))
        elif len(group) == 4:
            # Replace with a 2x2 brick (3003.DAT)
            color_id, x, y, z = group[0]
            replaced_bricks.append((color_id, x, y, z, "3003.DAT"))
        # I Need to add more conditions for larger groups
        else:
            # If not a known group, default to 1x1 bricks
            replaced_bricks.extend(group)

    return replaced_bricks
