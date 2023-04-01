set( headers bus.h startracker.h )
set( src bus.cpp startracker.cpp )

add_library( bus ${src} ${headers} )

target_include_directories( bus PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} )
target_compile_features( bus PUBLIC cxx_std_17) 
