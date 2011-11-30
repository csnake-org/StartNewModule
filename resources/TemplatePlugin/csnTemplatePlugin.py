# Used to configure TemplatePlugin
import csnBuild
import csnCilab
import csnUtility

# GIMIAS definitions
from csnGIMIASDef import *

# plugin project definition
templatePlugin = csnCilab.GimiasPluginProject("TemplatePlugin")
# plugin dependencies
projects = [
    gmCore, 
    guiBridgeLib, 
    baseLibVTK,
    guiBridgeLibWxWidgets
]
templatePlugin.AddProjects(projects)
# plugin sources
templatePlugin.AddSources(["*.cxx", "*.h"])
templatePlugin.AddIncludeFolders([])
templatePlugin.SetPrecompiledHeader("TemplatePluginPCH.h")
# plugin tests
templatePlugin.AddTests(["tests/*.*"], cxxTest)
