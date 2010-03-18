# Used to configure TemplateLibrary
import csnCilab
from csnCISTIBToolkit import *

templateLibrary = csnCilab.CilabModuleProject("TemplateLibrary", "library")
templateLibrary.AddLibraryModules(["tlFirst"])
templateLibrary.AddProjects([baseLib])
templateLibrary.AddTests(["tests/tlFirstTest/*.*"], cxxTest)
templateLibrary.SetPrecompiledHeader("TemplateLibraryPCH.h")