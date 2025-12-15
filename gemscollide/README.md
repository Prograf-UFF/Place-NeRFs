# GemsCollide: Fast Collision Detection of Moving Convex Polyhedra
The original code can be to found in [collide.c](https://github.com/erich666/GraphicsGems/blob/master/gemsiv/collide.c).
..

## Requirements
Make sure that you have the following tools before attempting to use GemsCollide.

Required tools:
- Your favorite [C++17](https://en.wikipedia.org/wiki/C%2B%2B17) compiler.
- [CMake](https://cmake.org/) (version >= 3.21) to automate installation and to build and run examples.

Required tools, if you want to use GemsCollide with Python:
- [Python 3.10](https://www.python.org/) interpreter, if you want to build and use GemsCollide with Python.

Required Python packages and C++ libraries, if you want to use GemsCollide with Python:
- [NumPy](https://numpy.org/), the fundamental package for scientific computing with Python.
- [Boost.Python](https://www.boost.org/users/history/version_1_75_0.html) (version == 1.75), a C++ library which enables seamless interoperability between C++ and the Python programming language.
- [Boost.NumPy](https://www.boost.org/doc/libs/release/libs/python/doc/html/numpy/index.html), a C++ library that extends Boost.Python to NumPy.

Optional tool to use GemsCollide with Python:
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) enviroment to create an isolated workspace for a Python application.

## How to Install Requirements in Linux
Requirements for the Linux operating system:
```console
$ sudo apt -y update --no-install-recommends 
$ sudo apt -y install --no-install-recommends build-essential wget g++ autotools-dev libicu-dev libbz2-dev libboost-all-dev
```

Install Python 3.10 (recomended) in your operating system or miniconda-environment. After, to use the commands presented bellow:
```console
$ pip --no-cache-dir install cmake==3.21.0 numpy
```

Install Boost.Python:
```console
$ wget https://boostorg.jfrog.io/artifactory/main/release/1.75.0/source/boost_1_75_0.tar.gz
$ tar -xzf boost_1_75_0.tar.gz
$ rm ./boost_1_75_0.tar.gz
$ cd ./boost_1_75_0
$ ./bootstrap.sh --prefix=/usr/ --with-libraries=python
$ ./b2 install
$ cd ..
$ rm -r ./boost_1_75_0
```

## How to Build and Install GemsCollide
Use the [git clone](https://git-scm.com/docs/git-clone) command to download the project, where <hilai360nerf-dir> must be replaced by the directory in which you want to place GemsCollide's source code, or remove <hilai360nerf-dir> from the command line to download the project to the ./hilai-360-nerf directory:
```console
$ git clone -b gemscollide https://github.com/Neural-Plant-Inspection/hilai-360-nerf.git <hilai360nerf-dir>
```
For now the code for `GemsCollide` is within project `hilai-360-nerf`.

Use CMake to copy GemsCollide's code files to the common include directory in your system (e.g., /usr/local/include, in Linux). The basic steps for installing GemsCollide/C++ using CMake look like this in Linux:
```console
$ cd <hilai360nerf-dir>/hilai360/gemscollide
$ mkdir build
$ cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
```

If there are problems with permissions, use `sudo` before `cmake`. The next command is used to work `sudo` and `cmake` together if there is some problem:
```console
$ sudo ln -s <cmake-install-prefix>/bin/cmake /usr/local/bin/cmake
```

Notice that you may use the -G <generator-name> option of CMake's command-line tool to choose the build system (e.g., Unix makefiles, Visual Studio, etc.). Please, refer to [CMake's Help](https://cmake.org/cmake/help/latest/manual/cmake.1.html) for a complete description of how to use the CMake's command-line tool.

After installation, CMake will find GemsCollide/C++ using the command find_package(GemsCollide) (see CMake documentation for details). In addition, you will be able to use the GEMSCOLLIDE_INCLUDE_DIRS variable in the CMakeList.txt file of your program while defining the include directories of your C++ project or targets.

GemsCollide/Python is a back-end to access GemsCollide/C++ from a Python environment. In this case, you have to build and install the GemsCollide/Python modules using the commands presented bellow:
```console
$ cmake --build . --config Release --parallel 8 --target install
```

It is important to emphasize that Python 3.10 is supported. Please, refer to [CMake's documentation](https://cmake.org/cmake/help/latest/module/FindPython.html) for details about how CMake finds the Python interpreter, compiler, and development environment.

Finally, add <cmake-install-prefix>/lib/gemscollide/python/<python-version> to the the PYTHONPATH environment variable. The <cmake-install-prefix> placeholder usually is `/usr/local` on Linux. But it may change according to what was set in CMake. The <python-version> placeholder is the version of the Python interpreter found by CMake.

Set the PYTHONPATH variable by calling following command in Linux:
```console
$ export PYTHONPATH="$PYTHONPATH:<cmake-install-prefix>/lib/gemscollide/python/<python-version>"
```

But this action is not permanent. The new value of PYTHONPATH will be lost as soon as you close the terminal. A possible solution to make an environment variable persistent for a user's environment is to export the variable from the user's profile script:

1. Open the current user's profile (the ~/.bash_profile file) into a text editor.
2. Add the export command for the PYTHONPATH environment variable at the end of this file.
3. Save your changes.

## How to Build and Install GemsCollide in Docker
Build docker image using the commands presented bellow:
```console
$ cd <hilai360nerf-dir>/hilai360/gemscollide
$ docker build -t gemscollide:latest .
```

All libraries and requirements are installed in the docker image. To run the container and install GemsCollide, just use the following commands:
```console
$ cd <hilai360nerf-dir>/hilai360/gemscollide
$ docker run --rm -it -v $PWD:/workspace gemscollide:latest bash
$ cd /workspace
$ bash build.sh
$ export PYTHONPATH="$PYTHONPATH:/usr/local/lib/gemscollide/python/3.8"
```
Revisar a versao do python: export PYTHONPATH="$PYTHONPATH:/usr/local/lib/gemscollide/python/$VERSAO"


## Running Examples
To-do..
```console
$ cd <hilai360nerf-dir>/hilai360/gemscollide/python/example
$ python example.py
```

```python
# Output:
number of tests = 30000
number of hits = 3160
```