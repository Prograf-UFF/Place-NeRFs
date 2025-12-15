import json, os
from model.place_nerfs import PlaceNeRFGraph


if __name__=="__main__":
    place_nerfs_far_distance = 4.56
    place_nerfs_add_new_nodes_to_communities = True
    place_nerfs_frames_json = '.data/visapp/london/frames.json'
    place_nerfs_path_result = os.path.dirname(place_nerfs_frames_json)

    place_nerfs = PlaceNeRFGraph()
    placed_nerfs, metrics = place_nerfs(None, None, None, 
                                        plan_of_irevest=None, 
                                        map_size=(0, 0), 
                                        far_distance=place_nerfs_far_distance, 
                                        place_nerfs_path_result=place_nerfs_path_result, 
                                        place_nerfs_frames_json=place_nerfs_frames_json,
                                        place_nerfs_add_new_nodes_to_communities=place_nerfs_add_new_nodes_to_communities
                                        )
    
    with open(os.path.join(place_nerfs_path_result, 'place_nerfs.json'), 'w') as file:
        data = []
        for nerf in placed_nerfs:
            data.append({
                'unit_id': nerf['unit_id'],
                'plant_id': nerf["plant_id"],
                'campaign_id': nerf['campaign_id'],
                'frames': [{'resource_id': frame['resource_id'], 
                            'new_node': frame['new_node'],
                            'world_position': frame['world_position'] if 'new_node' in frame else False} for frame in nerf['frames']],
                'views': [],
                'nerf_id': nerf['nerf_id'],
                'far_distance': nerf['far_distance'],
                'area_id': None
            })
        json.dump(data, file, indent=4)