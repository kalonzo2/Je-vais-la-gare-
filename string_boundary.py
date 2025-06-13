import trimesh
import numpy as np
from trimesh.creation import box
from trimesh.scene import Scene
from tqdm import tqdm  # For progress bar (optional but helpful)

def triangle_bounds(triangle):
    min_corner = np.min(triangle, axis=0)
    max_corner = np.max(triangle, axis=0)
    return min_corner, max_corner

def sample_point_in_triangle(v0, v1, v2):
    s, t = sorted(np.random.rand(2))
    return (1 - s) * v0 + (s - t) * v1 + t * v2

def create_voxel_cloud_on_triangle(triangle, count=1000, voxel_size=0.01):
    v0, v1, v2 = triangle
    voxels = []
    for _ in range(count):
        point = sample_point_in_triangle(v0, v1, v2)
        voxel = box(extents=[voxel_size]*3)
        voxel.apply_translation(point)
        voxels.append(voxel)
    return voxels

# Create a short fat cylinder
cylinder = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=24)

# Store all voxel meshes in a list
all_voxels = []

print("Generating voxel boxes for triangles...")

# Limit number of triangles for performance test
max_faces = 50  # adjust as needed
for face_index in tqdm(range(min(len(cylinder.faces), max_faces))):
    triangle = cylinder.triangles[face_index]
    voxel_boxes = create_voxel_cloud_on_triangle(triangle, count=1000, voxel_size=0.01)
    all_voxels.extend(voxel_boxes)

# Combine all voxel meshes into one
print("Combining voxel boxes into a single mesh...")
combined_mesh = trimesh.util.concatenate(all_voxels)

# Export to GLB and OBJ
print("Exporting...")
combined_mesh.export('string_endpoint_voxel.glb')
combined_mesh.export('string_endpoint_voxel.obj')

print("Export complete: 'string_endpoint_voxel.glb' and '.obj' written to disk.")