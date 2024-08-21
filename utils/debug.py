def debug_texture_application(mesh):
    if hasattr(mesh, 'textures') and mesh.textures is not None:
        print("Textures applied successfully.")
        print(f"Texture map size: {mesh.textures.maps_padded().shape}")
    else:
        print("Textures not applied to the mesh.")
