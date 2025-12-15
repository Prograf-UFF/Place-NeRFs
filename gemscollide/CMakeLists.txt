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

cmake_minimum_required(VERSION 3.14)

set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
set(VERSION_PATCH 20200604)

project(GEMSCOLLIDE
  VERSION ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}
  DESCRIPTION "GEMSCOLLIDE: Fast Collision Detection of Moving Convex Polyhedra"
  LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)



message(STATUS "Installing C++ front-end")

file(INSTALL ./cpp/include DESTINATION ${CMAKE_INSTALL_PREFIX} FILES_MATCHING PATTERN "*.cpp")

configure_file(./cmake/GEMSCOLLIDEConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/GEMSCOLLIDEConfig.cmake @ONLY NEWLINE_STYLE UNIX)
file(INSTALL ${CMAKE_CURRENT_BINARY_DIR}/GEMSCOLLIDEConfig.cmake DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/gemscollide)

configure_file(./cmake/GEMSCOLLIDEConfigVersion.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/GEMSCOLLIDEConfigVersion.cmake @ONLY NEWLINE_STYLE UNIX)
file(INSTALL ${CMAKE_CURRENT_BINARY_DIR}/GEMSCOLLIDEConfigVersion.cmake DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/gemscollide)

message(STATUS "Installing C++ front-end - done")



message(STATUS "Configuring Python front-end")

find_package(Python COMPONENTS Interpreter Development NumPy)
if(NOT Python_FOUND)
  message(STATUS "Configuring Python front-end - error (Python.Interpreter, Python.Developmemnt, or Python.NumPy components found)")
else()
  if(WIN32)
    set(Boost_USE_MULTITHREADED ON)
    set(Boost_USE_STATIC_LIBS OFF)
    add_definitions(-DBOOST_ALL_NO_LIB)
    add_definitions(-DBOOST_ALL_DYN_LINK)
  endif()

  foreach(_boost_python_suffix IN ITEMS "${Python_VERSION_MAJOR}${Python_VERSION_MINOR}" "${Python_VERSION_MAJOR}" "")
    find_package(Boost COMPONENTS python${_boost_python_suffix} numpy${_boost_python_suffix})
    if(Boost_FOUND)
      set(_boost_python_suffix_found ${_boost_python_suffix})
      break()
    endif()
  endforeach()

  if(NOT Boost_FOUND)
    message(STATUS "Configuring Python front-end - error (no matching Boost.Python or Boost.NumPy components found)")
  else()
    link_libraries(${Python_LIBRARIES} Boost::python${_boost_python_suffix_found} Boost::numpy${_boost_python_suffix_found} ${GEMSCOLLIDE_LIBRARIES})
    include_directories(${PROJECT_SOURCE_DIR}/python/module ${Python_INCLUDE_DIRS} ${Python_NumPy_INCLUDE_DIRS} ${Boost_INCLUDE_DIR} ${GEMSCOLLIDE_INCLUDE_DIRS})

    include(GNUInstallDirs)

    file(GLOB module_filenames RELATIVE ${PROJECT_SOURCE_DIR}/python/module ${PROJECT_SOURCE_DIR}/python/module/*.cpp)
    foreach(module_filename ${module_filenames})
      string(REPLACE ".cpp" "" module_name ${module_filename})
      Python_add_library(${module_name} ${PROJECT_SOURCE_DIR}/python/module/${module_filename})
      install(TARGETS ${module_name} LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/gemscollide/python/${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/gemscollide)
    endforeach()

    install(CODE "file(TOUCH \"${CMAKE_INSTALL_PREFIX}/lib/gemscollide/python/${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/gemscollide/__init__.py\")")
    message(STATUS "Configuring Python front-end - done")
  endif()

endif()


message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")