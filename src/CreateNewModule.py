import os.path

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
    
def EditFile(_source, _line, _type):
    assert os.path.exists(_source), "File not found: %s" % _source
    if( _type == 1 ):
        f = open(_source, 'a')
        f.write("\n%s" % _line); 
        f.close()
    if( _type == 2 ):
        f = open(_source, 'r')
        template = f.read() 
        f.close()
        template = template.replace( "])", ",%s\n])" % _line)
        f = open(_source, 'w')
        f.write(template)
        f.close()
    if( _type == 3 ):
        f = open(_source, 'r')
        template = f.read() 
        f.close()
        template = template.replace( "widgetModules = [", "widgetModules = [\n  '%s'," % _line)
        f = open(_source, 'w')
        f.write(template)
        f.close()
        

def CreateLibrary(_projectRoot, _libraryName, _rootForTemplateFiles):
    """ Create a new Library from template. """
    # check inputs
    assert len(_projectRoot) != 0
    assert len(_libraryName) != 0
    
    # create dictionary
    dictionary = dict()
    dictionary["TemplateLibrary"] = _libraryName;
    dictionary["TEMPLATELIBRARY"] = _libraryName.upper();
    dictionary["templateLibrary"] = _libraryName[ 0 ].lower( ) + _libraryName[ 1: ];

    # copy template files
    ConfigureFile("%s/TemplateLibrary/__init__.py" % _rootForTemplateFiles, "%s/%s/__init__.py" % (_projectRoot, _libraryName), dictionary)
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibrary.py" % _rootForTemplateFiles, "%s/%s/csn%s.py" % (_projectRoot, _libraryName, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibraryApps.py" % _rootForTemplateFiles, "%s/%s/csn%sApps.py" % (_projectRoot, _libraryName, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/TemplateLibraryPCH.h" % _rootForTemplateFiles, "%s/%s/%sPCH.h" % (_projectRoot, _libraryName, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/build/config.xml" % _rootForTemplateFiles, "%s/%s/build/config.xml" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/doc/Doxyfile.doxy" % _rootForTemplateFiles, "%s/%s/doc/Doxyfile.doxy" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/doc/Modules.dox" % _rootForTemplateFiles, "%s/%s/doc/Modules.dox" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/include/tlTemplate.h" % _rootForTemplateFiles, "%s/%s/libmodules/tlFirst/include/tlTemplate.h" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/src/tlTemplate.cpp" % _rootForTemplateFiles, "%s/%s/libmodules/tlFirst/src/tlTemplate.cpp" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/applications/tlAppFirst/tlAppFirst.cpp" % _rootForTemplateFiles, "%s/%s/applications/tlAppFirst/tlAppFirst.cpp" % (_projectRoot, _libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.h" % _rootForTemplateFiles, "%s/%s/tests/tlFirstTest/tlFirstTest.h" % (_projectRoot, _libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.cpp" % _rootForTemplateFiles, "%s/%s/tests/tlFirstTest/tlFirstTest.cpp" % (_projectRoot, _libraryName), dictionary)
    
    # append to toolkit file
    filename = "%s/../csnCISTIBToolkit.py" % (_projectRoot)
    assert os.path.exists(filename)
    EditFile(filename, "def %s():\n    import cilabModules.%s.csn%s\n    return cilabModules.%s.csn%s.%s" %(_libraryName[0].lower()+_libraryName[1:], _libraryName, _libraryName, _libraryName, _libraryName, _libraryName[0].lower()+_libraryName[1:]), 1)    

def CreatePlugin(_projectRoot, _pluginName, _rootForTemplateFiles):
    """ Create a new Plugin from template. """
    # check inputs
    assert len(_projectRoot) != 0
    assert len(_pluginName) != 0

    # create dictionary
    dictionary = dict()
    dictionary["TemplatePlugin"] = _pluginName;
    dictionary["templatePlugin"] = _pluginName[ 0 ].lower( ) + _pluginName[ 1: ];

    # copy template files
    ConfigureFile("%s/TemplatePlugin/build/config.xml" % _rootForTemplateFiles, "%s/%s/build/config.xml" % (_projectRoot, _pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/doc/Doxyfile.doxy" % _rootForTemplateFiles, "%s/%s/doc/Doxyfile.doxy" % (_projectRoot, _pluginName), dictionary)        
    ConfigureFile("%s/TemplatePlugin/doc/Modules.dox" % _rootForTemplateFiles, "%s/%s/doc/Modules.dox" % (_projectRoot, _pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/__init__.py" % _rootForTemplateFiles, "%s/%s/__init__.py" % (_projectRoot, _pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/csnTemplatePlugin.py" % _rootForTemplateFiles, "%s/%s/csn%s.py" % (_projectRoot, _pluginName, _pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/TemplatePlugin.cxx" % _rootForTemplateFiles, "%s/%s/%s.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePlugin.h" % _rootForTemplateFiles, "%s/%s/%s.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginPCH.h" % _rootForTemplateFiles, "%s/%s/%sPCH.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginProcessorCollective.cxx" % _rootForTemplateFiles, "%s/%s/%sProcessorCollective.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginProcessorCollective.h" % _rootForTemplateFiles, "%s/%s/%sProcessorCollective.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginWidgetCollective.cxx" % _rootForTemplateFiles, "%s/%s/%sWidgetCollective.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginWidgetCollective.h" % _rootForTemplateFiles, "%s/%s/%sWidgetCollective.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.cxx" % _rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.cxx" % (_projectRoot, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.h" % _rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.h" % (_projectRoot, _pluginName, _pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.cpp" % _rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.h" % _rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.cpp" % _rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.cpp" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.h" % _rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.h" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.wxg" % _rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.wxg" % (_projectRoot, _pluginName, _pluginName, _pluginName), dictionary)
    
    # append to toolkit files
    filename = "%s/../../csnCISTIBToolkit.py" % (_projectRoot)
    assert os.path.exists(filename)
    EditFile(filename, "def %s():\n    import Apps.Plugins.%s.csn%s\n    return Apps.Plugins.%s.csn%s.%s"  %(_pluginName[0].lower()+_pluginName[1:] , _pluginName, _pluginName, _pluginName, _pluginName, _pluginName[0].lower()+_pluginName[1:] ), 1)
    filename = "%s/../Gimias/csnGIMIAS.py" % (_projectRoot)
    assert os.path.exists(filename)
    EditFile(filename, "%s" % (_pluginName[0].lower()+_pluginName[1:] ), 2)

def CreatePluginWidget(_projectRoot, _pluginWidgetName, _rootForTemplateFiles):
    """ Create a new Widget from template. """
    # check inputs
    assert len(_projectRoot) != 0
    assert len(_pluginWidgetName) != 0

    # create dictionary
    dictionary = dict()
    dictionary["Sandbox"] = _pluginWidgetName;
    dictionary["sandbox"] = _pluginWidgetName[ 0 ].lower( ) + _pluginWidgetName[ 1: ];
    _pluginName = os.path.basename(_projectRoot)

    # copy template files
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.cxx" % _rootForTemplateFiles, "%s/processors/%s%sProcessor.cxx" % (_projectRoot, _pluginName, _pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.h" % _rootForTemplateFiles, "%s/processors/%s%sProcessor.h" % (_projectRoot, _pluginName, _pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.cpp" % _rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.cpp" % (_projectRoot, _pluginName, _pluginWidgetName, _pluginName, _pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.h" % _rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.h" % (_projectRoot, _pluginName, _pluginWidgetName, _pluginName, _pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.cpp" % _rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.cpp" % (_projectRoot, _pluginName, _pluginWidgetName, _pluginName, _pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.h" % _rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.h" % (_projectRoot, _pluginName, _pluginWidgetName, _pluginName, _pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.wxg" % _rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.wxg" % (_projectRoot, _pluginName, _pluginWidgetName, _pluginName, _pluginWidgetName), dictionary)
    
    # append to toolkit files
    filename = "%s/csn%s.py" % (_projectRoot, _pluginName)
    assert os.path.exists(filename)
    EditFile(filename, "%s%sPanelWidget" % (_pluginName, _pluginWidgetName ), 3)

