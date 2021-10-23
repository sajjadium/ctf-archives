cmake_minimum_required(VERSION 3.1)

set(project_name flag_server) ## rename your project here
project(${project_name})

set(CMAKE_CXX_STANDARD 11)

add_library(${project_name}-lib
        src/AppComponent.hpp
        src/controller/MyController.cpp
        src/controller/MyController.hpp
        src/dto/DTOs.hpp
)

# Decompression library
add_library(kylezip SHARED
        kylezip/decompress.c
)

set_target_properties(kylezip PROPERTIES LANGUAGE C)

## link libs

find_package(oatpp 1.2.5 REQUIRED)

target_link_libraries(${project_name}-lib
        PUBLIC oatpp::oatpp
        PUBLIC oatpp::oatpp-test
        kylezip
)

target_include_directories(${project_name}-lib PUBLIC src kylezip)

## add executables

add_executable(${project_name}-exe
        src/App.cpp
        test/app/MyApiTestClient.hpp)
target_link_libraries(${project_name}-exe ${project_name}-lib kylezip)

add_dependencies(${project_name}-exe ${project_name}-lib kylezip)

set_target_properties(${project_name}-lib ${project_name}-exe PROPERTIES
        CXX_STANDARD 11
        CXX_EXTENSIONS OFF
        CXX_STANDARD_REQUIRED ON
)

## add test executable


add_executable(kylezip-test
        kylezip/test/kyle.c
        )
target_link_libraries(kylezip-test kylezip)
