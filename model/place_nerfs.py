import time
import os.path as op
import networkx as nx
from scipy.spatial import distance
from scipy.spatial import Voronoi
import json, uuid, tqdm
import numpy as np
from typing import Callable, List, Tuple, Any
from gemscollide import collide

from utils.collide_utils import qvec2rotmat, camera_pyramid



class PlaceNeRFGraph(Callable[[], List[Any]]): 
    def __init__(self, **kwargs) -> None:
        super(PlaceNeRFGraph, self).__init__()

    def _public_process(self, frames, threshold, threshold_min_dist, place_nerfs_path_result, cam_intrinsics):
        num_ps = len(frames)
        # 1 - Distance pruning
        for idx1 in tqdm.tqdm(range(num_ps),  desc="    Distance Pruning"):
            for idx2 in tqdm.tqdm(range(idx1+1, num_ps),  desc=f"        Verifying distance pruning", leave=False):
                are_neighbors = False
                dist_ = distance.euclidean(self.ps_xyz[idx1], self.ps_xyz[idx2])
                if dist_ <= threshold:
                    are_neighbors = True
                self.neighbor[idx1, idx2] = are_neighbors
                self.neighbor[idx2, idx1] = are_neighbors

        # 1 - Visibility pruning   
        image_size = (cam_intrinsics['h'], cam_intrinsics['w'])
        fx,fy,cx,cy = cam_intrinsics['params']
        K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0,  0,  1]
        ])
        for idx1 in tqdm.tqdm(range(num_ps),  desc="    Visibility pruning (BATCH)"):
            distance_pruning = [x for x in np.where(self.neighbor[idx1])[0] if x>idx1] # escogemos solo los indices de los vecinos
            for idx2 in tqdm.tqdm(distance_pruning,  desc=f"        Verifying visibility pruning", leave=False):
                # a- Get views
                views = [frames[idx1]['resource_id'], frames[idx2]['resource_id']]
                
                # GEMSCOLLIDE 
                T = [np.array(frames[idx1]['tvec']), np.array(frames[idx2]['tvec'])]
                R = [qvec2rotmat(frames[idx1]['qvec']), qvec2rotmat(frames[idx2]['qvec'])]
                frustrum, py_txtytz = camera_pyramid(K, R, T, image_size=image_size, far=threshold, near=0.001)
                polyhedrons = [collide.init_polyhedron(poly.T.flatten(), 8, float(t[0]), float(t[1]), float(t[2])) for poly, t in list(zip(frustrum, py_txtytz))]  # init polyhedrons -- Pyramid=5 vertexs | frustum 8 vertexs
                couple = collide.init_couple(polyhedrons[0], polyhedrons[1])
                if not collide.Collision(couple): continue

                # Get depth-maps
                depths = [np.load(op.join(place_nerfs_path_result, 'depth', views[0][:-4]+'.npy')),
                          np.load(op.join(place_nerfs_path_result, 'depth', views[1][:-4]+'.npy')),]
                # c- Checking visibility
                dist_ = distance.euclidean(self.ps_xyz[idx1], self.ps_xyz[idx2])
                are_neighbors = depths[0].max()>dist_ and depths[1].max()>dist_
                self.neighbor[idx1, idx2] = are_neighbors
                self.neighbor[idx2, idx1] = are_neighbors
                if are_neighbors: self.edge_node.append((frames[idx1]['resource_id'],frames[idx2]['resource_id'], 1./dist_)) # (NodeA, NodeB, Weight)
                

    def _processing(self, 
                    unit_id:Any, 
                    plant_id:Any, 
                    campaign_id:Any, 
                    frames: List[Any], 
                    far_distance:float, 
                    image_processing_cubemap_size:int, 
                    image_processing_cubemap_fov:int,
                    image_processing_cubemap_theta_start:int,
                    image_processing_cubemap_theta_end:int,
                    image_processing_cubemap_theta_step:int,
                    area_id:str, 
                    min_fotosferas_valid_nerf: int=4,
                    louvain_resolution:float=1.0,
                    add_new_nodes_to_communities:bool=False,
                    place_nerfs_path_result:str=None,
                    place_nerf_batch_size:int=None, 
                    debug_path_save:str=None,
                    min_distance:float=None,
                    cam_intrinsics=None) -> List[Any]:
        num_ps = len(frames)
        frames_dict = dict() # para acessar mais rapido usando graphs (cada node 'e o resource_id)
        for frame in frames:
            frames_dict[frame['resource_id']] = frame
        # Trabalhamos em coordenadas do mundo
        self.ps_xyz = np.array([frame['world_position'] for frame in frames])

        # Geramos um grafo completo
        threshold = 2. * far_distance
        self.neighbor = np.zeros((num_ps, num_ps), dtype=np.bool_)
        self.edge_node = list()
        start = time.time()
        if plant_id is not None:
            pass
        else: # Public datasets
            self._public_process(frames, threshold, min_distance*4., place_nerfs_path_result, cam_intrinsics)
        print(f"   **TIME Building the visivility graph: {time.time()-start}")
        #return []

        # Calculamos as comunidades
        G = nx.Graph()
        G.add_weighted_edges_from(self.edge_node) #add_weighted_edges_from | add_edges_from
        communities_original = [list(comm) for comm in list(nx.community.louvain_communities(G, resolution=louvain_resolution, weight='weight', seed=42))] 
        communities = communities_original.copy()

        # Pos-procesamento das comunidades =================
        if add_new_nodes_to_communities:
            # Voronoi regions
            try:
                vor = Voronoi(self.ps_xyz)
            except Exception as e:
                ps_xyz_2d = np.array([xyz[:2] for xyz in self.ps_xyz])
                vor = Voronoi(ps_xyz_2d)

            # Create graph from voronoi
            GDelaunay = nx.Graph()
            # Voronoi foi criado no ordem dos Frames, "ridge_points" representa o Delaunay
            GDelaunay.add_edges_from([[frames[u]['resource_id'],frames[v]['resource_id']] for u,v in vor.ridge_points])

            new_neighbors = dict()
            for i in range(len(communities)):
                tmp = dict()
                for j in range(0,len(communities)):
                    if i==j: continue
                    new_nodes = []
                    # encontrando vizinho no maximo um grado
                    for u in communities[j]:
                        has_edge = [G.has_edge(u, v) and GDelaunay.has_edge(u, v) for v in communities[i]].count(True) > 0
                        if has_edge: new_nodes.append(u)
                    tmp[j] = new_nodes
                new_neighbors[i] = tmp
            # agregando novos vizinhos
            for i in range(len(communities)):
                communities[i] = communities[i] + sum(list(new_neighbors[i].values()),[])
            

        if place_nerfs_path_result is not None:
            #from .plot_utils import plot_graph_community
            #plot_graph_community(unit_id, plant_id, G, frames_dict, communities_original, place_nerfs_path_result, aspect_ratio='auto')
            # Agregando atributo 'X,Y,Z' ao graph.graphml para fins de plot e debug posterior
            for node in G.nodes:
                x,y,z = frames_dict[node]['world_position']
                G.nodes[node]['X'] = x
                G.nodes[node]['Y'] = y
                G.nodes[node]['Z'] = z
            nx.write_graphml_lxml(G, op.join(place_nerfs_path_result, "graph.graphml"))

        # Cada NeRF vai ser uma comunidade =====================================
        nerfs: List[Any] = list()
        for idx,community in enumerate(communities):
            nerf_frames: List[Any] = list()
            nerf_views: List[Any] = list()
            if len(community)<min_fotosferas_valid_nerf: continue
            for node in community:
                # Agregamos uma etiqueta ao frame para saber se 'e um novo nodo agregado fora da comunidade original
                is_new_node = False if node in communities_original[idx] else True
                nerf_frames.append({'resource_id':node ,'new_node': is_new_node, 'world_position': frames_dict[node]['world_position']}) 
                # Geramos oss views para cada fotosfera
                if plant_id is not None: # nerf_views - pode ser util em ambemtes industrials
                    pass
                    
            nerfs.append({'unit_id': unit_id, 
                    'plant_id': plant_id,
                    'campaign_id':campaign_id,
                    'frames':nerf_frames,
                    'views':nerf_views,
                    'nerf_id': uuid.uuid4().hex,
                    'nerf_radius': 0, 
                    'far_distance': far_distance,
                    'area_id':area_id,
                    'location_in_px':None} )
        return nerfs


    def __call__(self, unit_id: Any, plant_id: Any, campaign_id: Any, *, 
                 map_size: Tuple[Any, Any], 
                 far_distance: float, 
                 nerf_radius: float=0., 
                 plan_of_irevest: Any=None, 
                 image_processing_cubemap_theta_start: int=0, 
                 image_processing_cubemap_theta_end: int=360, 
                 image_processing_cubemap_theta_step: int=90, 
                 image_processing_cubemap_phi_start: int=0, 
                 image_processing_cubemap_phi_end: int=45, 
                 image_processing_cubemap_phi_step: int=45, 
                 image_processing_cubemap_size: int=960, 
                 image_processing_cubemap_fov: float=90.0, 
                 place_nerfs_min_fotosferas_valid_nerf: int=3, 
                 plant_name: str=None,
                 place_nerfs_add_new_nodes_to_communities:bool=False,
                 place_nerfs_louvain_resolution:float=1.0, 
                 place_nerfs_path_result:str=None,
                 place_nerf_batch_size:int=None, 
                 place_nerfs_debug_plot_path:str=None,
                 place_nerfs_frames_json:str=None, **kwargs) -> List[Any]:
        if plan_of_irevest is None:
            with open(place_nerfs_frames_json, 'r') as f:
                frames_json = json.load(f)
            divided_subregions = self._processing(unit_id, plant_id, campaign_id, 
                                                  frames=frames_json['frames'],
                                                  far_distance=far_distance, 
                                                  image_processing_cubemap_size=0, 
                                                  image_processing_cubemap_fov=0,
                                                  image_processing_cubemap_theta_start=0,
                                                  image_processing_cubemap_theta_end=0,
                                                  image_processing_cubemap_theta_step=0,
                                                  area_id=None, 
                                                  min_fotosferas_valid_nerf=place_nerfs_min_fotosferas_valid_nerf,
                                                  louvain_resolution=place_nerfs_louvain_resolution,
                                                  add_new_nodes_to_communities=place_nerfs_add_new_nodes_to_communities,
                                                  place_nerfs_path_result=place_nerfs_path_result,
                                                  place_nerf_batch_size=place_nerf_batch_size,
                                                  debug_path_save=None,
                                                  min_distance=frames_json['min_distance'],
                                                  cam_intrinsics=frames_json["cam_intrinsics"])
            
            return divided_subregions, {}
        else:
            pass