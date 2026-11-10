cmake_minimum_required(VERSION 3.19...4.4)
project(EmbeddedPython LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
include(FetchContent)
FetchContent_Declare(
  pybind11
  URL           https://github.com/pybind/pybind11/archive/refs/tags/v3.1.0.tar.gz
  URL_HASH      SHA256=ef712655692a2e9bf7bb7874c022564a45f91d847ddee987e720cd9e28849665
  DOWNLOAD_NO_PROGRESS
)
FetchContent_MakeAvailable(pybind11)

add_executable(embedded_python embedded_python.cpp)
target_link_libraries(embedded_python PRIVATE pybind11::embed)
