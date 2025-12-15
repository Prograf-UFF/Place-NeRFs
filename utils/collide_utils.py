import math
import numpy as np
from typing import List, Tuple


def get_frustum(intrinsic:np.ndarray, extrinsic:np.ndarray, image_size:Tuple[int, int], far:float, near:float, bbox=None) -> np.ndarray:
    h, w = image_size
    xy_img = np.asarray([[0, 0, 1], [w-1, 0, 1], [w-1, h-1, 1], [0, h-1, 1]], dtype=np.float32).T
    xyz_cam = np.matmul(np.linalg.inv(intrinsic), xy_img)
    eye_cam = np.asarray([[0, 0, 0, 1]], dtype=np.float32).T

    # TEST work in meters
    xyz_world = np.concatenate((xyz_cam, [[1,1,1,1]]), axis=0).T @ extrinsic.T 
    eye_world = eye_cam.T @ extrinsic.T
    
    dir2 = xyz_world.T - eye_world.T
    dir2 /= np.linalg.norm(dir2, ord=2, axis=0)

    far_vertices = xyz_world + (math.sqrt(3.0) * far) * dir2.T
    near_vertices = xyz_world + (math.sqrt(3.0) * near) * dir2.T

    vertex_std = np.concatenate((near_vertices, far_vertices), axis=0) 
    
    return vertex_std

def camera_pyramid(K:np.ndarray, R:List[np.ndarray], T:List[np.ndarray], image_size, far:float, near:float):
    original, center, txtytz = [], [], []
    for i in range(len(R)):
        extrinsic = np.concatenate((R[i], np.array([T[i]]).T), axis=1)
        extrinsic = np.concatenate((extrinsic, [[0.,0.,0.,1.]]), axis=0)

        vertex_transformed = get_frustum(K, extrinsic, image_size, far, near, None) # shape(5,4)
        original.append(vertex_transformed)
        vertex_transformed = vertex_transformed[:,:-1].T #remove last column # shape(3,5)
        means = np.mean(vertex_transformed, axis=1)
        center.append(vertex_transformed - means[:,np.newaxis])
        txtytz.append(means)
    return center, txtytz
