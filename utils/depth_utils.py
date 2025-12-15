import numpy as np
import argparse
import os, json
from tqdm import tqdm
from utils.colmap_read_model import read_model, qvec2rotmat
from itertools import combinations


def project_point(K, qvec, tvec, point3D):
    """
    # Exemplo de parâmetros
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0,  0,  1]
    ])

    qvec = np.array([q0, q1, q2, q3])  # da imagem
    tvec = np.array([tx, ty, tz])      # da imagem
    point3D = np.array([X, Y, Z])      # ponto 3D

    x, y = project_point(K, qvec, tvec, point3D)
    print(f"Coordenadas na imagem: x={x:.2f}, y={y:.2f}")
    """
    R = qvec2rotmat(qvec)
    Rt = np.hstack((R, tvec.reshape(3, 1)))  # [R | t]
    P = K @ Rt  # Projeção completa

    X = np.append(point3D, 1)  # Homogêneo
    x_proj = P @ X
    x_proj /= x_proj[2]  # Normaliza

    return x_proj[0], x_proj[1]  # Coordenadas (x, y)


def get_depthmaps(key, images, cameras, points3D):
    image_meta = images[key]
    cam_intrinsic = cameras[image_meta.camera_id]

    R = qvec2rotmat(image_meta.qvec)
    t = image_meta.tvec
    P = np.hstack((R, t.reshape(3, 1)))  # Projection matrix
    C = -R.T @ t  # Camera center
    depth_map = []

    fx, fy, cx, cy = cam_intrinsic.params
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0,  0,  1]
    ])
    depth_debug = [] #np.zeros((cam_intrinsic.height, cam_intrinsic.width), dtype=float)

    for i, (x, y) in enumerate(image_meta.xys):
        point3D_id = image_meta.point3D_ids[i]
        if point3D_id == -1:
            depth_map.append(0)
            continue
        X = points3D[point3D_id].xyz
        depth = np.linalg.norm(X - C)
        depth_map.append(depth)

        #_x, _y = project_point(K, image_meta.qvec, image_meta.tvec, points3D[point3D_id].xyz) # to deebug
        depth_debug.append((y,x, depth))

    """cmap = matplotlib.cm.jet
    cmap.set_bad('white',1.)
    cmap_r = matplotlib.cm.jet_r
    cmap_r.set_bad('white',1.)
    cmap_ = matplotlib.cm.gray
    cmap_.set_bad('white',1.)
    tmp = np.array(depth_debug).T
    plt.scatter(tmp[1], tmp[0], c=tmp[2], cmap=cmap_r, s=1)"""
    return np.array(depth_map)


def get_frames_and_depth_sparse(args):
    cam_intrinsics, images_metas, points3d = read_model(os.path.join(args.base_dir, "sparse", "0"), ext=f".{args.model_type}")

    #pts_indices = np.array([points3d[key].id for key in points3d])
    #pts_xyzs = np.array([points3d[key].xyz for key in points3d])
    #points3d_ordered = np.zeros([pts_indices.max()+1, 3])
    #points3d_ordered[pts_indices] = pts_xyzs
    
    # Generate frames file ===================================================
    frames = []
    # Calcula posições absolutas das câmeras
    positions = []
    for key in images_metas:
        R = qvec2rotmat(images_metas[key].qvec)
        C = -R.T @ images_metas[key].tvec
        positions.append(C)
        frames.append({"resource_id":images_metas[key].name, "world_position":C.tolist(), 'qvec':images_metas[key].qvec.tolist(), 'tvec':images_metas[key].tvec.tolist()})
    # Calcula distâncias entre todas as posições
    distances = [np.linalg.norm(p1 - p2) for p1, p2 in combinations(positions, 2)]
    pass
    cam = [{"model":cam_intrinsics[key].model, 
            "w":cam_intrinsics[key].width, 
            "h": cam_intrinsics[key].height, 
            "params": cam_intrinsics[key].params.tolist()} for key in cam_intrinsics] 
    with open(os.path.join(args.base_dir, "frames.json"), 'w') as json_file:
        data = {'cam_intrinsics': cam[0], 
                'min_distance':min(distances), 
                'max_distance': max(distances), 
                'mean_distance': np.mean(distances), 
                'frames': frames}
        json.dump(data, json_file, indent=4)
    # ============================================================================

    # create depth maps
    path_depth = os.path.join(args.base_dir, 'depth')
    if not os.path.exists(path_depth): os.makedirs(path_depth, exist_ok=True)
    for key in tqdm(images_metas):
        depth = get_depthmaps(key, images_metas, cam_intrinsics, points3d) 
        np.save(os.path.join(args.base_dir, 'depth', f'{images_metas[key].name[:-4]}.npy'), depth)
        

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default="data/nyc")
    parser.add_argument('--model_type', default="bin")
    args = parser.parse_args()

    get_frames_and_depth_sparse(args)