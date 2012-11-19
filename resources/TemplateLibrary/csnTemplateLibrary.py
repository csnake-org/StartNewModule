# CSNake configuration of the Template library

# CSNake imports
from csnAPIPublic import GetAPI
api = GetAPI("2.5.0")
# Other dependencies
from csnToolkitOpen import *

# Definition of the template library
templateLibrary = api.CreateStandardModuleProject("TemplateLibrary", "library")
templateLibrary.AddLibraryModules(["tlFirst"])
templateLibrary.AddProjects([baseLib])
templateLibrary.AddTests(["tests/tlFirstTest/*.*"], cxxTest)
templateLibrary.SetPrecompiledHeader("TemplateLibraryPCH.h")
