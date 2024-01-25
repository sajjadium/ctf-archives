cmake_minimum_required(VERSION 3.15)
project(webserver VERSION 0.0.1)

set(CMAKE_CXX_STANDARD 20)

if(APPLE)
set(CMAKE_OSX_DEPLOYMENT_TARGET 12.0)
endif()

# JUCE.
set(JUCE_BUILD_EXTRAS OFF)
set(JUCE_BUILD_EXAMPLES OFF)
set(JUCE_USE_MP3AUDIOFORMAT ON)

add_subdirectory(juce)

juce_add_console_app(${PROJECT_NAME}
    PRODUCT_NAME "relay")     # The name of the final executable, which can differ from the target name

    target_compile_definitions(${PROJECT_NAME}
    PRIVATE
        # JUCE_WEB_BROWSER and JUCE_USE_CURL would be on by default, but you might not need them.
        JUCE_WEB_BROWSER=0  # If you remove this, add `NEEDS_WEB_BROWSER TRUE` to the `juce_add_console_app` call
        JUCE_USE_CURL=0    # If you remove this, add `NEEDS_CURL TRUE` to the `juce_add_console_app` call
        JUCE_USE_XRANDR=0
        JUCE_USE_XINERAMA=0
        JUCE_USE_XCURSOR=0
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE
        # ConsoleAppData            # If you'd created a binary data target, you'd link to it here
        juce::juce_core
        juce::juce_audio_formats
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_warning_flags)


# Find the Drogon package
find_package(Drogon CONFIG REQUIRED)

# Link against the Drogon library
target_link_libraries(${PROJECT_NAME} PRIVATE Drogon::Drogon)

# Set the output directory for the binary
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)


# Find source files.
file(GLOB_RECURSE SOURCE_FILES CONFIGURE_DEPENDS src/*.cpp src/*.cc)
target_sources(${PROJECT_NAME} PRIVATE ${SOURCE_FILES})


aux_source_directory(controllers CTL_SRC)
aux_source_directory(filters FILTER_SRC)
aux_source_directory(plugins PLUGIN_SRC)
aux_source_directory(models MODEL_SRC)

file(GLOB SCP_LIST ${CMAKE_CURRENT_SOURCE_DIR}/views/*.csp)
foreach(cspFile ${SCP_LIST})
    message(STATUS "cspFile:" ${cspFile})
    EXEC_PROGRAM(basename ARGS "${cspFile} .csp" OUTPUT_VARIABLE classname)
    message(STATUS "view classname:" ${classname})
    ADD_CUSTOM_COMMAND(OUTPUT ${classname}.h ${classname}.cc
            COMMAND drogon_ctl
            ARGS create view ${cspFile}
            DEPENDS ${cspFile}
            VERBATIM )
    set(VIEW_SRC ${VIEW_SRC} ${classname}.cc)
endforeach()

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/models)
target_sources(${PROJECT_NAME} PRIVATE ${SRC_DIR} ${CTL_SRC} ${FILTER_SRC} ${VIEW_SRC} ${PLUGIN_SRC} ${MODEL_SRC})

set_property(TARGET ${PROJECT_NAME} PROPERTY ENABLE_EXPORTS ON)
