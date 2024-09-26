cmake_minimum_required(VERSION 3.18...3.25)
project(Minuit2SimpleExamle LANGUAGES CXX)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)
FetchContent_Declare(
  minuit2
  URL           https://github.com/root-project/root/archive/refs/tags/v6-26-10.tar.gz
  URL_HASH      SHA256=a84ed095252614c6e2084987fce9ce4a5a62057bfd5a4a2725123ca9f60f674f
  SOURCE_SUBDIR math/minuit2
  DOWNLOAD_NO_PROGRESS
  EXCLUDE_FROM_ALL
)
FetchContent_MakeAvailable(minuit2)

if(NOT DEFINED SKBUILD)
  add_executable(simpleminuit app/simpleminuit.cpp app/SimpleFCN.h)
  target_include_directories(simpleminuit PRIVATE ${minuit2_SOURCE_DIR})
  target_link_libraries(simpleminuit PRIVATE Minuit2::Minuit2)
else()
  find_package(pybind11)

  file(GLOB OUTPUT src/*.cpp)
  pybind11_add_module(minuit2 ${OUTPUT})
  target_link_libraries(minuit2 PUBLIC Minuit2::Minuit2)

  install(TARGETS minuit2 DESTINATION ${SKBUILD_PLATLIB_DIR} COMPONENT python)
endif()
