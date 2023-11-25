
set(HDD_IMAGE_FILE_SRC "${CMAKE_CURRENT_LIST_DIR}/SWEB-flat.vmdk.tar.gz")
set(HDD_IMAGE_FILE ${PROJECT_BINARY_DIR}/SWEB-flat.vmdk)

#Custom Command: Outputs empty ext2 disk image
add_custom_command (OUTPUT ${HDD_IMAGE_FILE}
  COMMAND ${CMAKE_COMMAND} -E tar xzf "${HDD_IMAGE_FILE_SRC}"
  DEPENDS "${HDD_IMAGE_FILE_SRC}"
  WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
  COMMENT "Unpacking disk image..."
  )

add_custom_target(blank_hdd_image DEPENDS ${HDD_IMAGE_FILE})
