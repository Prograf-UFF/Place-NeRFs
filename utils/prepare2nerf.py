import shutil
import os, json
import argparse


def run_system_command(cmd_with_args: str):
        err = os.system(cmd_with_args)
        if err:
            raise RuntimeError(f"System-Command has failed after running {cmd_with_args}.")

def discarted_images(all_imgs_list, conservar_imgs_list, path_save):
    descartar = list(set(all_imgs_list) - set(conservar_imgs_list))
    with open(path_save, "w") as file:
        for line in descartar:
            file.write(line + "\n") 


def generate_comunities_to_trainnerf(base_dir:str, my_nerf_id:str=None):
    place_nerfs_json = os.path.join(base_dir, 'place_nerfs.json')
    # Confirmamos se os arquivos json existem
    if not os.path.isfile(place_nerfs_json): raise FileNotFoundError(f"{place_nerfs_json} was not found or is a directory")

    # Open expected views for each NeRF.
    with open(place_nerfs_json, 'r') as place_nerfs_file:
        place_nerfs_data = json.load(place_nerfs_file)
    img_path = os.path.join(base_dir, 'images') 
    submodel = 'sparse/0'
    for nerf in place_nerfs_data:
        nerf_id = nerf['nerf_id']
        if my_nerf_id is not None:
            if nerf_id!=my_nerf_id: continue
        nerf_path_imgs = os.path.join(os.path.dirname(base_dir), nerf_id,'images')
        os.makedirs(nerf_path_imgs, exist_ok=True)
        conservar = list()
        for frame in nerf['frames']:
            conservar.append(frame['resource_id'])
            shutil.copy(os.path.join(img_path, frame['resource_id']), os.path.join(nerf_path_imgs, frame['resource_id']))

        imgs_path_discarted = os.path.join(os.path.dirname(base_dir), nerf_id,'discarted_images.txt')
        discarted_images(os.listdir(img_path), conservar, imgs_path_discarted)
        output = os.path.join(os.path.dirname(base_dir), nerf_id, submodel)
        os.makedirs(output, exist_ok=True)
        run_system_command(f'colmap image_deleter --input_path {os.path.join(base_dir, submodel)} --output_path {output}  --image_names_path {imgs_path_discarted}')
        
        # without neightbors
        """nerf_without_path_imgs = os.path.join(os.path.dirname(base_dir), nerf_id+"_without",'images')
        os.makedirs(nerf_without_path_imgs, exist_ok=True)
        conservar_wo = list()
        for frame in nerf['frames']:
            if frame['new_node']==False:
                conservar_wo.append(frame['resource_id'])
                shutil.copy(os.path.join(img_path, frame['resource_id']), os.path.join(nerf_without_path_imgs, frame['resource_id']))

        imgs_path_discarted_wo = os.path.join(os.path.dirname(base_dir), nerf_id+"_without",'discarted_images.txt')
        discarted_images(os.listdir(img_path), conservar_wo, imgs_path_discarted_wo)
        output_wo = os.path.join(os.path.dirname(base_dir), nerf_id+"_without", submodel)
        os.makedirs(output_wo, exist_ok=True)
        run_system_command(f'colmap image_deleter --input_path {os.path.join(base_dir, submodel)} --output_path {output_wo}  --image_names_path {imgs_path_discarted_wo}')
        """

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default="data/nyc")
    parser.add_argument('--nerf_id', default=None)
    args = parser.parse_args()

    generate_comunities_to_trainnerf(args.base_dir, args.nerf_id)