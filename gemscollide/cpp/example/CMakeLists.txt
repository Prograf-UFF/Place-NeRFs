# Copyright (C) 2019 Leandro Augusto Frata Fernandes
# 
# authors    : TODO
# 
# repository : https://github.com/erich666/GraphicsGems/blob/master/gemsiv/collide.c
# 
# C code from the article
# "Fast Collision Detection of Moving Convex Polyhedra"
# by Rich Rabbitz, rrabbitz%pgn138fs@serling.motown.ge.com
# in "Graphics Gems IV", Academic Press, 1994
#
# 

cmake_minimum_required(VERSION 3.10)

project(GEMSCOLLIDE-Example)

find_package(GEMSCOLLIDE REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(target_prefix gemscollide_example_)

include_directories(${GEMSCOLLIDE_INCLUDE_DIRS})

file(GLOB example_filenames RELATIVE "${PROJECT_SOURCE_DIR}" ${PROJECT_SOURCE_DIR}/*.c)
foreach(example_filename ${example_filenames})
  string(REPLACE ".cpp" "" example_name ${example_filename})
  add_executable(${target_prefix}${example_name} "${PROJECT_SOURCE_DIR}/${example_filename}")
  target_include_directories(${target_prefix}${example_name} PUBLIC ${PROJECT_SOURCE_DIR})
  target_link_libraries(${target_prefix}${example_name})
endforeach()