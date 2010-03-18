import os.path
import sys

def ConfigureFile(_source, _dest, _dict):
    assert os.path.exists(_source), "File not found: %s" % _source
    f = open(_source, 'r')
    template = f.read()        
    f.close()
    
    os.path.exists(os.path.dirname(_dest)) or os.makedirs(os.path.dirname(_dest))
    for varName in _dict.keys():
        template = template.replace("%s" % varName, _dict[varName])
    f = open(_dest, 'w')
    f.write(template)
    f.close()

def CreateLibrary(_projectRoot, _libraryName, _rootForTemplateFiles):
    dictionary = dict()
    dictionary["TemplateLibrary"] = _libraryName;
    dictionary["TEMPLATELIBRARY"] = _libraryName.upper();
    dictionary["templateLibrary"] = _libraryName[ 0 ].lower( ) + _libraryName[ 1: ];

    ConfigureFile("%s/TemplateLibrary/__init__.py" % _rootForTemplateFiles, "%s/cilabModules/%s/__init__.py" % (_projectRoot, _libraryName), dictionary)
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibrary.py" % _rootForTemplateFiles, "%s/cilabModules/%s/csn%s.py" % (_projectRoot, _libraryName, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibraryApps.py" % _rootForTemplateFiles, "%s/cilabModules/%s/csn%sApps.py" % (_projectRoot, _libraryName, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/TemplateLibraryPCH.h" % _rootForTemplateFiles, "%s/cilabModules/%s/%sPCH.h" % (_projectRoot, _libraryName, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/build/config.xml" % _rootForTemplateFiles, "%s/cilabModules/%s/build/config.xml" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/doc/Doxyfile.doxy" % _rootForTemplateFiles, "%s/cilabModules/%s/doc/Doxyfile.doxy" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/doc/Modules.dox" % _rootForTemplateFiles, "%s/cilabModules/%s/doc/Modules.dox" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/include/tlTemplate.h" % _rootForTemplateFiles, "%s/cilabModules/%s/libmodules/tlFirst/include/tlTemplate.h" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/src/tlTemplate.cpp" % _rootForTemplateFiles, "%s/cilabModules/%s/libmodules/tlFirst/src/tlTemplate.cpp" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/applications/tlAppFirst/tlAppFirst.cpp" % _rootForTemplateFiles, "%s/cilabModules/%s/applications/tlAppFirst/tlAppFirst.cpp" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.h" % _rootForTemplateFiles, "%s/cilabModules/%s/tests/tlFirstTest/tlFirstTest.h" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.cpp" % _rootForTemplateFiles, "%s/cilabModules/%s/tests/tlFirstTest/tlFirstTest.cpp" % (_projectRoot, _libraryName), dictionary)        

def CreatePlugin(_projectRoot, _pluginName, _rootForTemplateFiles):
    dictionary = dict()
    dictionary["SandboxPlugin"] = _pluginName;
    dictionary["sandboxPlugin"] = _pluginName[ 0 ].lower( ) + _pluginName[ 1: ];

    ConfigureFile("%s/TemplatePlugin/build/config.xml" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/build/config.xml" % (_projectRoot, _pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/doc/Doxyfile.doxy" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/doc/Doxyfile.doxy" % (_projectRoot, _pluginName), dictionary)        
    ConfigureFile("%s/TemplatePlugin/doc/Modules.dox" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/doc/Modules.dox" % (_projectRoot, _pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/__init__.py" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/__init__.py" % (_projectRoot, _pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/csnSandboxPlugin.py" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/csn%s.py" % (_projectRoot, _pluginName, _pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/SandboxPlugin.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%s.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPlugin.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%s.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPluginPCH.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%sPCH.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPluginProcessorCollective.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%sProcessorCollective.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPluginProcessorCollective.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%sProcessorCollective.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPluginWidgetCollective.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%sWidgetCollective.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/SandboxPluginWidgetCollective.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/%sWidgetCollective.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginResampleProcessor.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sResampleProcessor.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginResampleProcessor.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sResampleProcessor.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginShapeScaleProcessor.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sShapeScaleProcessor.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginShapeScaleProcessor.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sShapeScaleProcessor.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginSubtractProcessor.cxx" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sSubtractProcessor.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/SandboxPluginSubtractProcessor.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/processors/%sSubtractProcessor.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginShapeScalePanelWidget/SandboxPluginShapeScalePanelWidget.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sShapeScalePanelWidget/%sShapeScalePanelWidget.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginShapeScalePanelWidget/SandboxPluginShapeScalePanelWidget.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sShapeScalePanelWidget/%sShapeScalePanelWidget.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginShapeScalePanelWidget/SandboxPluginShapeScalePanelWidgetUI.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sShapeScalePanelWidget/%sShapeScalePanelWidgetUI.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginShapeScalePanelWidget/SandboxPluginShapeScalePanelWidgetUI.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sShapeScalePanelWidget/%sShapeScalePanelWidgetUI.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginShapeScalePanelWidget/SandboxPluginShapeScalePanelWidgetUI.wxg" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sShapeScalePanelWidget/%sShapeScalePanelWidgetUI.wxg" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginResamplePanelWidget/SandboxPluginResamplePanelWidget.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sResamplePanelWidget/%sResamplePanelWidget.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginResamplePanelWidget/SandboxPluginResamplePanelWidget.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sResamplePanelWidget/%sResamplePanelWidget.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginResamplePanelWidget/SandboxPluginResamplePanelWidgetUI.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sResamplePanelWidget/%sResamplePanelWidgetUI.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginResamplePanelWidget/SandboxPluginResamplePanelWidgetUI.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sResamplePanelWidget/%sResamplePanelWidgetUI.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginResamplePanelWidget/SandboxPluginResamplePanelWidgetUI.wxg" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sResamplePanelWidget/%sResamplePanelWidgetUI.wxg" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginSubtractPanelWidget/SandboxPluginSubtractPanelWidget.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sSubtractPanelWidget/%sSubtractPanelWidget.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginSubtractPanelWidget/SandboxPluginSubtractPanelWidget.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sSubtractPanelWidget/%sSubtractPanelWidget.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginSubtractPanelWidget/SandboxPluginSubtractPanelWidgetUI.cpp" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sSubtractPanelWidget/%sSubtractPanelWidgetUI.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginSubtractPanelWidget/SandboxPluginSubtractPanelWidgetUI.h" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sSubtractPanelWidget/%sSubtractPanelWidgetUI.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/SandboxPluginSubtractPanelWidget/SandboxPluginSubtractPanelWidgetUI.wxg" % _rootForTemplateFiles, "%s/Apps/Plugins/%s/widgets/%sSubtractPanelWidget/%sSubtractPanelWidgetUI.wxg" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
