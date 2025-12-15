Instalacao
conda create

recomenddado usar ockerfile do GemsCollide

pip install -r requiremments.txt


Experimentos com datasets publicos

baixar os datasets publicos, exemplo NYC
Tem as imagens e o modelo esparso

Extrair os ddedpthmaps sparsos
python ./utils/depth_utils.py --base_dir data/nyc/

issso gera o frameees.json e os mapas dee profundidaed

Eexecutar python main.py --base_dir data/nyc/

Executar python prepare2nerf.py --base_dir data/nyc/

prepare para treinammeento do NeRF
python ./utils/prepare2nerf.py --base_dir data/nyc/ --nerf_id <NeRF-ID>