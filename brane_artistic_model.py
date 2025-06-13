import numpy as np
import trimesh

# CREATE BOX
def create_box():
    vertices = np.array([
        [0, 0, 0],
        [-7, 50, 7],
        [7, -7, -7],
        [10, 0, 0],
        [
        ])
    faces = np.array([[0, 1, 2]])
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

# CALCULATE POSITIONS
def calculate_positions(n):
    rows = int(np.ceil((-1 + np.sqrt(1 + 6 * n)) / 2))
    positions = []
    count = 0
    for i in range(rows):
        for j in range(i + 1):
            if count < n:
                positions.append([j, 0, i])
                count += 1
    return np.array(positions)

# CREATE SCENE
def create_scene(n):
    scene = trimesh.Scene()
    box = create_box()
    positions = calculate_positions(n)
    for pos in positions:
        box_copy = box.copy()
        box_copy.apply_translation(pos)
        scene.add_geometry(box_copy)
    return scene

# EXPORT SCENE
def export_scene(n, filename):
    scene = create_scene(n)
    scene.export(filename)
    print(f"Exported {n} boxes to '{filename}'")

# EXECUTE
if __name__ == "__main__":
    export_scene(10000, 'triangular_structure.glb')
