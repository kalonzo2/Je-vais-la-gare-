import trimesh
import numpy as np
from trimesh.creation import box
from trimesh.scene import Scene

def triangle_bounds(triangle):
    # Calculate the bounding box of a triangle
    min_corner = np.min(triangle, axis=0)
    max_corner = np.max(triangle, axis=0)
    return min_corner, max_corner

def sample_point_in_triangle(v0, v1, v2):
    # Sample uniformly within triangle using barycentric coordinates
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

# Create short cylinder (fat disk)
cylinder = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=24)

scene = Scene()

# For each triangle in the cylinder mesh, add voxel boxes
for face_index in range(len(cylinder.faces)):
    triangle = cylinder.triangles[face_index]
    voxel_boxes = create_voxel_cloud_on_triangle(triangle, count=1000, voxel_size=0.01)
    for vb in voxel_boxes:
        scene.add_geometry(vb)

# Show the scene
scene.show()