PROJECT(TemplateThirdParty)

REGISTER_THIRDPARTY_PROJECT_NAME(TemplateThirdParty
  "TemplateThirdParty libraries and headers."
)

IF(WIN32)
    SET(TemplateThirdParty_LIBRARY_DIRS
      "${${PROJECT_NAME}_SOURCE_DIR}/lib"
    )

    SET(TemplateThirdParty_INCLUDE_DIRS
      "${${PROJECT_NAME}_SOURCE_DIR}/include"
    )
    SET(TemplateThirdParty_LIBRARIES
      # here goes the name of your lib files
	  optimized "myLibName"
      # here goes the name of your debug lib files
	  debug "myLibName"
    )

ELSE(WIN32)

    MESSAGE(SEND_ERROR 
      "TemplateThirdParty not implemented for Linux."
    )
  
ENDIF(WIN32)

# Location of the TemplateThirdParty use file.
SET(TemplateThirdParty_USE_FILE "${${PROJECT_NAME}_BINARY_DIR}/Use${PROJECT_NAME}.cmake")

CONFIGURE_FILE(
  "${${PROJECT_NAME}_SOURCE_DIR}/${PROJECT_NAME}Config.cmake.in"
  "${${PROJECT_NAME}_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
  @ONLY
  IMMEDIATE
)

CONFIGURE_FILE(
  "${${PROJECT_NAME}_SOURCE_DIR}/Use${PROJECT_NAME}.cmake.in"
  "${${PROJECT_NAME}_BINARY_DIR}/Use${PROJECT_NAME}.cmake"
  COPYONLY
)

