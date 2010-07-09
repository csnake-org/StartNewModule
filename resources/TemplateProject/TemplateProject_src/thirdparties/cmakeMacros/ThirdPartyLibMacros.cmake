MACRO(CLEAR_VARIABLE ARGV1)
  SET(${ARGV1}
    ""
  )
ENDMACRO(CLEAR_VARIABLE ARGV1)

MACRO(CLEAR_CACHED_VARIABLE ARGV1)
  SET(${ARGV1}
    ""
    CACHE
    INTERNAL
    ""
    FORCE
  )
ENDMACRO(CLEAR_CACHED_VARIABLE ARGV1)

# argv1 = project name
# argv2 = project description
# This function also sets the XXX_DIR value (where XXX is the project name).

MACRO(REGISTER_THIRDPARTY_PROJECT_NAME ARGV1 ARGV2)
  # add project name to AVAILABLE_THIRDPARTY_PROJECTS
  IF(NOT AVAILABLE_THIRDPARTY_PROJECTS MATCHES "${ARGV1} : ")
    SET(AVAILABLE_THIRDPARTY_PROJECTS
      "\n${ARGV1} : ${ARGV2}"
      ${AVAILABLE_THIRDPARTY_PROJECTS}
      CACHE
      INTERNAL
      ""
      FORCE
    )
  ENDIF(NOT AVAILABLE_THIRDPARTY_PROJECTS MATCHES "${ARGV1} : ")
  
  # Make sure that each package in the THIRDPARTY_PROJECTS_NAME
  # list appears only once. There is no operation in the 
  # list to search for an item (until cmake 2.4-7) so
  # we first try remove it and then we add it. That way
  # we know that appears only once. Then we put it in the cache.
  LIST(LENGTH
    THIRDPARTY_PROJECTS_NAME
    THIRDPARTY_PROJECTS_NAME_LENGTH
  )
  IF(THIRDPARTY_PROJECTS_NAME_LENGTH)
    LIST(REMOVE_ITEM
      THIRDPARTY_PROJECTS_NAME
      "${ARGV1}"
    )
  ENDIF(THIRDPARTY_PROJECTS_NAME_LENGTH)

  LIST(APPEND
    THIRDPARTY_PROJECTS_NAME
    "${ARGV1}"
  )
  
  # store THIRDPARTY_PROJECTS_NAME in the cache
  SET(THIRDPARTY_PROJECTS_NAME
    ${THIRDPARTY_PROJECTS_NAME}
    CACHE
    INTERNAL
    ""
    FORCE
  )
  # We define for each ${THIRDPARTY_MODULE} the ${THIRDPARTY_MODULE}_DIR. When
  # someone does a FIND_PACKAGE(${THIRDPARTY_MODULE}) the macro will search
  # for the ${THIRDPARTY_MODULE}_DIR directory. That's why we export this information.
  IF(NOT "${ARGV1}_DIR")
    SET("${ARGV1}_DIR"
      "${CILAB_TOOLKIT_BINARY_DIR}/${ARGV1}"
      CACHE
      INTERNAL
      "Path to the ${ARGV1}"
     )
  ENDIF(NOT "${ARGV1}_DIR")
ENDMACRO(REGISTER_THIRDPARTY_PROJECT_NAME ARGV1 ARGV2)

# First parameter will be the projects name, and the rest of the parameters
# will be the projects from which this project depends from.
MACRO(REGISTER_THIRDPARTY_PROJECT_DEPENDENCIES)

  # Read current project name from the parameter list
  # and take it out. The project names left on the variable
  # will belong to the projects from which it depends.
  SET(ARGUMENT_LIST
    ${ARGV}
  )
  LIST(GET
    ARGUMENT_LIST
    0
    CURRENT_PROJECT_NAME
  )
  LIST(REMOVE_AT
    ARGUMENT_LIST
    0
  )
  FOREACH(PROJECT_NAME ${ARGUMENT_LIST})
    SET(${CURRENT_PROJECT_NAME}_DEPENDS_FROM
      ${PROJECT_NAME}
      ${${CURRENT_PROJECT_NAME}_DEPENDS_FROM}
      CACHE
      INTERNAL
      "Cilab Projects from which ${CURRENT_PROJECT_NAME} depends."
      FORCE
    )
  ENDFOREACH(PROJECT_NAME ${ARGUMENT_LIST})
ENDMACRO(REGISTER_THIRDPARTY_PROJECT_DEPENDENCIES)

# Accepts a project name. 
# Adds the project name to the CILAB_TOOLKIT_TO_BE_COMPILED list.
# If this project depends on other projects (${${ARGV}_DEPENDS_FROM} is not empty)
# then the macro calls itself (recursion) on each item in ${${ARGV}_DEPENDS_FROM}.

MACRO(RECURSE_DEPENDENCIES ARGV)
  IF(${ARGV}_DEPENDS_FROM)
    FOREACH(DEPENDENCY ${${ARGV}_DEPENDS_FROM})
      RECURSE_DEPENDENCIES(${DEPENDENCY})
    ENDFOREACH(DEPENDENCY ${${ARGV}_DEPENDS_FROM})
  ENDIF(${ARGV}_DEPENDS_FROM)

  LIST(APPEND
    CILAB_TOOLKIT_TO_BE_COMPILED
    ${ARGV}
  )
ENDMACRO(RECURSE_DEPENDENCIES)

# This macro processes the ${CILAB_PROJECTS_CHOOSEN}
# to decide which project to compile. To do this, every
# project defines its ${PROJECT_NAME}_DEPENDS_FROM variable
# which contains the names of the projects from which it depends.
MACRO(RESOLVE_DEPENDENCIES)

  CLEAR_VARIABLE(CILAB_TOOLKIT_TO_BE_COMPILED)
  IF(CILAB_PROJECTS_CHOOSEN)
    FOREACH(PROJECT ${CILAB_PROJECTS_CHOOSEN})
      RECURSE_DEPENDENCIES(${PROJECT})
    ENDFOREACH(PROJECT ${CILAB_PROJECTS_CHOOSEN})
  ENDIF(CILAB_PROJECTS_CHOOSEN)

  # Order packages so MITK is the first to be compiled 
  # and DCMTK be the last one to be compiled.
  ORDER_PACKAGES(CILAB_TOOLKIT_TO_BE_COMPILED)

ENDMACRO(RESOLVE_DEPENDENCIES)

# Some packages like DCMTK, ITK, VTK, MITK have strange of
# erroneous befaviour when configured before or after one 
# of the other packages in the list. After try n error 
# found out that the order to be correctly configured and
# compiled is the one forced above. Always MITK before ITK
# and always DCMTK the last package to be configured!!!!!
MACRO(ORDER_PACKAGES PACKAGE_LIST)

  # If found MITK or CoreLib that has MITK in its include dirs
  # put it in the first position of the package list.
  FOREACH(PACKAGE ${${PACKAGE_LIST}})
    IF(${PACKAGE} MATCHES "MITK*")
      LIST(REMOVE_ITEM
        ${PACKAGE_LIST}
        ${PACKAGE}
      )
      LIST(APPEND
        ${PACKAGE_LIST}
        ${PACKAGE}
      )
    ENDIF(${PACKAGE} MATCHES "MITK*")

    IF(${PACKAGE} MATCHES "CoreLib*")
      LIST(REMOVE_ITEM
        ${PACKAGE_LIST}
        ${PACKAGE}
      )
      LIST(INSERT
        ${PACKAGE_LIST}
        0
        ${PACKAGE}
      )
    ENDIF(${PACKAGE} MATCHES "CoreLib*")

    # If found DCMTK remove it from the list and append it in
    # the last position of the package list.
    IF(${PACKAGE} MATCHES "DCMTK*")
      LIST(REMOVE_ITEM
        ${PACKAGE_LIST}
        ${PACKAGE}
      )
      LIST(APPEND
        ${PACKAGE_LIST}
        "${PACKAGE}"
      )
    ENDIF(${PACKAGE} MATCHES "DCMTK*")
  ENDFOREACH(PACKAGE)

ENDMACRO(ORDER_PACKAGES)

# Apply qt patch to avoid configuration warning. This patch saves the QTDIR
# environment variable during the CILab Toolkit configuration and in the end,
# the END_QT_PATCH recovers the original value. This patch is only applied in
# windows machines.
MACRO(START_QT_PATCH)
  IF(WIN32)
    SET(QTDIR_TMP
      $ENV{QTDIR}
    )
    SET(ENV{QTDIR}
      ${CILAB_TOOLKIT_SOURCE_DIR}/QT-3.3.7/qt-win-free-3.3.7
    )
  ENDIF(WIN32)
ENDMACRO(START_QT_PATCH)

# End QT patch. Recover the original value of the QTDIR environment variable
# to the value before the configuration.
MACRO(END_QT_PATCH)
  IF(WIN32)
    SET(ENV{QTDIR}
      ${QTDIR_TMP}
    )
  ENDIF(WIN32)
ENDMACRO(END_QT_PATCH)
