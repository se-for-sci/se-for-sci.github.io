cmake_minimum_required(VERSION 3.19...3.27)
project(EmbeddedPython LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
include(FetchContent)
FetchContent_Declare(
  pybind11
  URL           https://github.com/pybind/pybind11/archive/refs/tags/v2.11.1.tar.gz
  URL_HASH      SHA256=d475978da0cdc2d43b73f30910786759d593a9d8ee05b1b6846d1eb16c6d2e0c
  DOWNLOAD_NO_PROGRESS
)
FetchContent_MakeAvailable(pybind11)

add_executable(embedded_python embedded_python.cpp)
target_link_libraries(embedded_python PRIVATE pybind11::embed)
