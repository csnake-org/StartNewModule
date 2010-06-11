# Used to configure TemplatePlugin
import csnBuild
import csnCilab
import csnUtility

from csnGIMIASDef import *

templatePlugin = csnCilab.GimiasPluginProject("TemplatePlugin")

projects = [
    gmCore, 
    guiBridgeLib, 
    baseLibVTK,
    guiBridgeLibWxWidgets
]
templatePlugin.AddProjects(projects)

templatePlugin.AddSources(["*.cxx", "*.h"])
templatePlugin.AddSources(["processors/*.cxx", "processors/*.h"])
templatePlugin.AddIncludeFolders(["processors"])

widgetModules = [
#  "TemplatePluginSandboxPanelWidget"
  ]
templatePlugin.AddWidgetModules(widgetModules, _useQt = 0)

templatePlugin.SetPrecompiledHeader("TemplatePluginPCH.h")

templatePlugin.AddTests(["tests/*.*"], cxxTest)