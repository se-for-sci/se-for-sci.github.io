cmake_minimum_required(VERSION 3.18...4.4)
project(Minuit2SimpleExample LANGUAGES CXX)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)
FetchContent_Declare(
  minuit2
  URL           https://github.com/root-project/root/archive/refs/tags/v6-40-04.tar.gz
  URL_HASH      SHA256=02b994fd645dbb7b89f5ab9342278d3c53bf2ed46d50aebd1aecccfa040711c4
  SOURCE_SUBDIR math/minuit2
  DOWNLOAD_NO_PROGRESS
  EXCLUDE_FROM_ALL
)
set(minuit2_standalone ON CACHE BOOL "Copy in the needed ROOT headers" FORCE)
FetchContent_MakeAvailable(minuit2)

if(NOT DEFINED SKBUILD)
  add_executable(simpleminuit app/simpleminuit.cpp app/SimpleFCN.h)
  target_include_directories(simpleminuit PRIVATE ${minuit2_SOURCE_DIR})
  target_link_libraries(simpleminuit PRIVATE Minuit2::Minuit2)
else()
  find_package(pybind11 CONFIG REQUIRED)

  file(GLOB OUTPUT src/*.cpp)
  pybind11_add_module(minuit2 ${OUTPUT})
  target_link_libraries(minuit2 PUBLIC Minuit2::Minuit2)

  install(TARGETS minuit2 DESTINATION ${SKBUILD_PLATLIB_DIR} COMPONENT python)
endif()
