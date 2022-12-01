cmake_minimum_required(VERSION 3.19...3.25)
project(EmbeddedPython LANGUAGES CXX)

include(FetchContent)
FetchContent_Declare(
  pybind11
  URL           https://github.com/pybind/pybind11/archive/refs/tags/v2.10.1.tar.gz
  URL_HASH      SHA256=111014b516b625083bef701df7880f78c2243835abdb263065b6b59b960b6bad
  DOWNLOAD_NO_PROGRESS
)
FetchContent_MakeAvailable(pybind11)

add_executable(embedded_python embedded_python.cpp)
target_link_libraries(embedded_python PRIVATE pybind11::embed)
