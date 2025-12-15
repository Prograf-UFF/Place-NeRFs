import json, os
import argparse
from model.place_nerfs import PlaceNeRFGraph


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default="data/nyc")
    parser.add_argument('--far_distance', default=4.39)
    parser.add_argument('--improve_frontiers', default=True)
    args = parser.parse_args()

    place_nerfs_far_distance = args.far_distance
    place_nerfs_add_new_nodes_to_communities = args.improve_frontiers
    place_nerfs_frames_json = os.path.join(args.base_dir,'frames.json')
    place_nerfs_path_result = os.path.dirname(place_nerfs_frames_json)

    place_nerfs = PlaceNeRFGraph()
    placed_nerfs, _ = place_nerfs(None, None, None, 
                                        plan_of_irevest=None, 
                                        map_size=(0, 0), 
                                        far_distance=place_nerfs_far_distance, 
                                        place_nerfs_path_result=place_nerfs_path_result, 
                                        place_nerfs_frames_json=place_nerfs_frames_json,
                                        place_nerfs_add_new_nodes_to_communities=place_nerfs_add_new_nodes_to_communities
                                        )
    
    # Save place-nerfs.json file
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
                'far_distance': nerf['far_distance']
            })
        json.dump(data, file, indent=4)