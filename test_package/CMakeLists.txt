cmake_minimum_required(VERSION 3.10)
project(PackageTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Qt5 REQUIRED COMPONENTS Core)

add_executable(example example.cpp)

target_link_libraries(example
    PRIVATE
        CONAN_PKG::qsqlcipher
        Qt5::Core)
