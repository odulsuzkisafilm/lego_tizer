def parse_mtl(mtl_path):
    material = {}
    current_material = None
    with open(mtl_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('newmtl'):
                current_material = line.split()[1]
                material[current_material] = {}
            elif current_material:
                if line.startswith('map_') or line.startswith('bump'):
                    key = line.split()[0]
                    texture_file = line.split()[-1]
                    material[current_material][key] = texture_file
                elif line.startswith('Kd'):
                    material[current_material]['color'] = [float(v) * 255 for v in line.split()[1:]]

    return material
