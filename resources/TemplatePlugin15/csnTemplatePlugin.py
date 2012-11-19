# CSNake configuration of the TemplatePlugin

# CSNake imports
from csnAPIPublic import GetAPI
api = GetAPI("2.5.0")
# Other dependencies
from csnGIMIASDef import *
from csnToolkitOpen import * 

# Definition of the template plugin
templatePlugin = GimiasPluginProject("TemplatePlugin", api)
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
templatePlugin.SetPrecompiledHeader("TemplatePluginPCH.h")
# plugin tests
templatePlugin.AddTests(["tests/*.*"], cxxTest)
