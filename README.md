# Place-NeRFs: A smart approach to divide large and complex scenes into multiple regions of locally related views

Place-NeRFs is a scalable approach for large-scale 3D scene reconstruction that intelligently subdivides scenes into non-overlapping regions, allowing each region to be handled independently by off-the-shelf Neural Radiance Field (NeRF) models.


## Overview

The codebase has 3 main process:
- Extracting depth maps from the COLMAP sparse model;
- Processing our Place-NeRFs approach,
- Prepare the Place-NeRFs output to be used in NeRF training.

For these experiments we use public datasets that can be found on [SMeRF-3D](https://smerf-3d.github.io/#data).


## Platforms
We have compiled and tested the sample application on Linux andd Windows using Python 3.8 and COLMAP 3.12.

## Requirements
Make sure that you have all the following tools and libraries installed and working before attempting to compile.

Required tools:
- [Python](https://pt.wikipedia.org/wiki/Python) 3.8 or later (Linux or Windows)
- [COLMAP](https://colmap.github.io/) 3.12 or later (Linux or Windows)
- [GemsCollide](gemscollide/README.md) (Linux or Windows)
- [Docker](https://www.docker.com/) (Optional)

Required Python packages:
- [NetworkX](https://networkx.org/en/) 3.6.1 or later 
- [SciPy](https://www.scipy.org/about.html) 0.17 or later
- [Tqdm](https://pypi.org/project/tqdm/) 4.67.1 or later
- [NumPy](https://www.numpy.org/) 1.11 or later
- [Matplotlib](https://matplotlib.org/) 3.0.3 or later

## Building, Compiling, and Running
Use the [git clone](https://git-scm.com/docs/git-clone) command to download the project:

```shell
# HTTPS
$ git clone https://github.com/Prograf-UFF/Place-NeRFs.git 
$ cd Place-NeRFs
```

Extracting depth maps from the COLMAP sparse model:
```shell
$ python ./utils/depth_utils.py --base_dir <path to COLMAP>
```

The `depth_utils.py` script generates the depthmaps files in `.npy` format and the `frames.json` file (which contains information about the images).Then, we run our Place-NeRFs approach:
```shell
$ python main.py --base_dir <path to COLMAP> --far_distance <far value>
```

Place-NeRFs generates the file `place_nerfs.json`, where all generated communities are saved, and each community has an identifier `nerf_id`. Each community is used to train a NeRF. The following command is used to prepare the necessary files for training one community with a NeRF.
```shell
$ python ./utils/prepare2nerf.py --base_dir data/nyc/ --nerf_id <NeRF-ID>
```

## Funding and Acknowledgments
This research work was conducted in association with the Petrobras R\&D project (SAP \#4600671059 and \#4600684055) in accordance with the regulations on investments in research, development, and innovation by the Brazilian National Petroleum Agency (ANP). The author acknowledges support from CNPq (302938/2025-7). Jose L. Huillca was sponsored by a CAPES fellowship.
