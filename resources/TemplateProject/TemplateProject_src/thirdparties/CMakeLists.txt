# This is the root CMakeLists.txt cmake file to build
# the entire toolkit developed in the Cilab laboratory.

PROJECT(CILAB_TOOLKIT)

# This is the minimum required version to configure the Toolkit
CMAKE_MINIMUM_REQUIRED(VERSION 2.4.5)

INCLUDE("${CILAB_TOOLKIT_SOURCE_DIR}/cmakeMacros/ThirdPartyLibMacros.cmake")
INCLUDE("${CILAB_TOOLKIT_SOURCE_DIR}/cmakeMacros/PlatformDependent.cmake")

# Apply qt patch to avoid configuration warning. This patch saves the QTDIR
# environment variable during the CILab Toolkit configuration and in the end,
# the END_QT_PATCH recovers the original value. This patch is only applied in
# windows machines.
START_QT_PATCH()

# Use own patched Find<PackageName> instead of the default of CMake.
SET(CMAKE_MODULE_PATH
  "${CILAB_TOOLKIT_SOURCE_DIR}/cmakeMacros"
)

###############################################################
# Set the folder of the thirdparty project

CLEAR_VARIABLE(CILAB_PROJECTS_CHOOSEN)

# CMP0013: Duplicate binary directories are not allowed.
# This CMakeLists.txt parses two times the subdirs
IF(COMMAND CMAKE_POLICY)
  CMAKE_POLICY(SET CMP0013 OLD)
ENDIF(COMMAND CMAKE_POLICY)


# default lib and exe dir
SET(CILAB_THIRDPARTY_LIBRARY_OUTPUT_PATH "${CILAB_TOOLKIT_BINARY_DIR}/lib")
SET(CILAB_THIRDPARTY_EXECUTABLE_OUTPUT_PATH "${CILAB_TOOLKIT_BINARY_DIR}/bin")

###############################################################
# Get dependencies for each project
FOREACH(CILAB_THIRDPARTY ${AVAILABLE_THIRDPARTY})
    CLEAR_VARIABLE(${CILAB_THIRDPARTY}_TO_BE_COMPILED)
    # restore the output paths before every project because some of them overwrite it, which might confuse
    # projects defined afterwards (so order of projects matters, which is bad)
    SET(LIBRARY_OUTPUT_PATH "${CILAB_THIRDPARTY_LIBRARY_OUTPUT_PATH}")
    SET(EXECUTABLE_OUTPUT_PATH "${CILAB_THIRDPARTY_EXECUTABLE_OUTPUT_PATH}")
    ADD_SUBDIRECTORY("${CILAB_THIRDPARTY}")
    SET(CILAB_PROJECTS_CHOOSEN
      ${CILAB_THIRDPARTY}
      ${CILAB_PROJECTS_CHOOSEN}
    )
ENDFOREACH(CILAB_THIRDPARTY)


###############################################################
# Resolve dependencies
RESOLVE_DEPENDENCIES()


###############################################################
# Configure each project
IF(CILAB_TOOLKIT_TO_BE_COMPILED)
  
  # while there are projects to compile (here compile means: generate vcproj (windows) or makefile (linux)
  CLEAR_VARIABLE(EMPTY_TO_BE_COMPILED)
  WHILE(NOT EMPTY_TO_BE_COMPILED)

    # Get first element of the projects to be compiled list
    LIST(GET
      CILAB_TOOLKIT_TO_BE_COMPILED
      0
      CURRENT_PROJECT
    )
    # Erease every instance of the element in the list.
    LIST(REMOVE_ITEM
      CILAB_TOOLKIT_TO_BE_COMPILED
      "${CURRENT_PROJECT}"
    )
    
    SET( CURRENT_PROJECT_PATH ${${CURRENT_PROJECT}_SOURCE_DIR} )
    
    # The project is not compiled here, but in a different cmake script.
    # This other cmake script will inspect if ${CURRENT_PROJECT}_TO_BE_COMPILED is defined 
    # to see if it must compile the project. Therefore, define this value here.
    SET(${CURRENT_PROJECT}_TO_BE_COMPILED "TRUE" CACHE STRING "" FORCE )

    SET(${CURRENT_PROJECT}_PATH "${CURRENT_PROJECT_PATH}" CACHE STRING "" FORCE )
    
    # Restore the output paths before every project because some of them overwrite it,
    # which might confuse projects defined afterwards.
    # (so order of projects matters, which is bad)

    # clean up cmake vars
    SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CILAB_THIRDPARTY_LIBRARY_OUTPUT_PATH}")
    SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CILAB_THIRDPARTY_EXECUTABLE_OUTPUT_PATH}")
    SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CILAB_THIRDPARTY_LIBRARY_OUTPUT_PATH}")
    # clean up lib specific vars
    SET(LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
    SET(RUNTIME_OUTPUT_DIRECTORY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
    SET(ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}")
    # clean up old vars
    SET(LIBRARY_OUTPUT_PATH "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
    SET(EXECUTABLE_OUTPUT_PATH "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
    # clean up shared libs
    CLEAR_VARIABLE(BUILD_SHARED_LIBS)
    
    # Add the third party
    MESSAGE( STATUS "Parsing ${CURRENT_PROJECT} to be compiled..." )
    ADD_SUBDIRECTORY(${CURRENT_PROJECT_PATH})
    
    # Clear this variable afterwards to get rid of some warning messages.
    CLEAR_VARIABLE(${CURRENT_PROJECT}_TO_BE_COMPILED)

    IF(NOT CILAB_TOOLKIT_TO_BE_COMPILED)
      SET(EMPTY_TO_BE_COMPILED "TRUE")
    ENDIF(NOT CILAB_TOOLKIT_TO_BE_COMPILED)
  ENDWHILE(NOT EMPTY_TO_BE_COMPILED)
ENDIF(CILAB_TOOLKIT_TO_BE_COMPILED)

INCLUDE("${CILAB_TOOLKIT_SOURCE_DIR}/cmakeMacros/ResetCachedValues.cmake")

# End QT patch. Recover the original value of the QTDIR environment variable
# to the value before the configuration.
END_QT_PATCH()

