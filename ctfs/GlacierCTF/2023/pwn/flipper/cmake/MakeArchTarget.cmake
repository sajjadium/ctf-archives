# Macro for defining the "make ${ARCH}" targets
#
# If you want to add a target with multiple variable definitions, this is how you do it:
# MAKE_ARCH_TARGET(my_arch my/arch "-DVAR1=VALUE1;-DVAR2=VALUE2;...")

function(MAKE_ARCH_TARGET TARGET_NAME ARCH_NAME EXTRA_FLAGS)
  add_custom_target(${TARGET_NAME}
      COMMAND ${PROJECT_SOURCE_DIR}/utils/prompt.sh "rm -fR ${PROJECT_BINARY_DIR}/*: remove all arguments recursively [Y/n]? "
      COMMAND rm -fR ${PROJECT_BINARY_DIR}/* || true
      COMMAND cmake -DARCH="${ARCH_NAME}" ${EXTRA_FLAGS} ${PROJECT_SOURCE_DIR} ${CMAKE_CROSS_COMPILE_FLAGS}
  )
endfunction(MAKE_ARCH_TARGET)
