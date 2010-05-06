import os.path

def ConfigureFile(source, dest, dict):
    """ Replace string in source file according to a dictionary. """
    # check source file
    if not os.path.exists(source):
        raise IOError("File not found: %s" % source)
    # read the source file
    f = open(source, 'r')
    template = f.read()        
    f.close()
    # replace strings according to the dictionary
    for varName in dict.keys():
        template = template.replace("%s" % varName, dict[varName])
    # create path to dest if not there
    os.path.exists(os.path.dirname(dest)) or os.makedirs(os.path.dirname(dest))
    # write destination file
    f = open(dest, 'w')
    f.write(template)
    f.close()
    
def EditFile(source, line, type):
    """ Append line to a file according to type."""
    # check source file
    if not os.path.exists(source):
        raise IOError("File not found: %s" % source)
    # type 1: main csn file
    if( type == 1 ):
        f = open(source, 'a')
        f.write("\n%s" % line); 
        f.close()
    # type 2: gimias csn file
    if( type == 2 ):
        f = open(source, 'r')
        template = f.read() 
        f.close()
        template = template.replace( "])", ",%s\n])" % line)
        f = open(source, 'w')
        f.write(template)
        f.close()
    # type 3: widget file
    if( type == 3 ):
        f = open(source, 'r')
        template = f.read() 
        f.close()
        template = template.replace( "widgetModules = [", "widgetModules = [\n  '%s'," % line)
        f = open(source, 'w')
        f.write(template)
        f.close()      

def CreateLibrary(rootPath, libraryName, rootForTemplateFiles, tkFilename):
    """ Create a new Library from template. """
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(libraryName) == 0:
        raise ValueError("No library name provided.")
    if not os.path.exists(tkFilename):
        raise IOError("The toolkit csnake file does not exist.")
    
    # create dictionary
    dictionary = dict()
    dictionary["TemplateLibrary"] = libraryName;
    dictionary["TEMPLATELIBRARY"] = libraryName.upper();
    dictionary["templateLibrary"] = libraryName[ 0 ].lower( ) + libraryName[ 1: ];

    # copy template files
    ConfigureFile("%s/TemplateLibrary/__init__.py" % rootForTemplateFiles, "%s/%s/__init__.py" % (rootPath, libraryName), dictionary)
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibrary.py" % rootForTemplateFiles, "%s/%s/csn%s.py" % (rootPath, libraryName, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/csnTemplateLibraryApps.py" % rootForTemplateFiles, "%s/%s/csn%sApps.py" % (rootPath, libraryName, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/TemplateLibraryPCH.h" % rootForTemplateFiles, "%s/%s/%sPCH.h" % (rootPath, libraryName, libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/build/config.xml" % rootForTemplateFiles, "%s/%s/build/config.xml" % (rootPath, libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/doc/Doxyfile.doxy" % rootForTemplateFiles, "%s/%s/doc/Doxyfile.doxy" % (rootPath, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/doc/MainPage.dox" % rootForTemplateFiles, "%s/%s/doc/MainPage.dox" % (rootPath, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/doc/Modules.dox" % rootForTemplateFiles, "%s/%s/doc/Modules.dox" % (rootPath, libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/include/tlTemplate.h" % rootForTemplateFiles, "%s/%s/libmodules/tlFirst/include/tlTemplate.h" % (rootPath, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/libmodules/tlFirst/src/tlTemplate.cpp" % rootForTemplateFiles, "%s/%s/libmodules/tlFirst/src/tlTemplate.cpp" % (rootPath, libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/applications/tlAppFirst/tlAppFirst.cpp" % rootForTemplateFiles, "%s/%s/applications/tlAppFirst/tlAppFirst.cpp" % (rootPath, libraryName), dictionary)        

    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.h" % rootForTemplateFiles, "%s/%s/tests/tlFirstTest/tlFirstTest.h" % (rootPath, libraryName), dictionary)        
    ConfigureFile("%s/TemplateLibrary/tests/tlFirstTest/tlFirstTest.cpp" % rootForTemplateFiles, "%s/%s/tests/tlFirstTest/tlFirstTest.cpp" % (rootPath, libraryName), dictionary)
    
    # append to toolkit file
    EditFile(tkFilename, "def %s():\n    import cilabModules.%s.csn%s\n    return cilabModules.%s.csn%s.%s" %(libraryName[0].lower()+libraryName[1:], libraryName, libraryName, libraryName, libraryName, libraryName[0].lower()+libraryName[1:]), 1)    

def CreatePlugin(rootPath, pluginName, rootForTemplateFiles, tkFilename, gimiasFilename):
    """ Create a new Plugin from template. """
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(pluginName) == 0:
        raise ValueError("No plugin name provided.")
    if not os.path.exists(tkFilename):
        raise IOError("The toolkit csnake file does not exist.")
    if not os.path.exists(gimiasFilename):
        raise IOError("The gimias csnake file does not exist.")

    # create dictionary
    dictionary = dict()
    dictionary["TemplatePlugin"] = pluginName;
    dictionary["templatePlugin"] = pluginName[ 0 ].lower( ) + pluginName[ 1: ];

    # copy template files
    ConfigureFile("%s/TemplatePlugin/build/config.xml" % rootForTemplateFiles, "%s/%s/build/config.xml" % (rootPath, pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/doc/Doxyfile.doxy" % rootForTemplateFiles, "%s/%s/doc/Doxyfile.doxy" % (rootPath, pluginName), dictionary)        
    ConfigureFile("%s/TemplatePlugin/doc/MainPage.dox" % rootForTemplateFiles, "%s/%s/doc/MainPage.dox" % (rootPath, pluginName), dictionary)        
    ConfigureFile("%s/TemplatePlugin/doc/Modules.dox" % rootForTemplateFiles, "%s/%s/doc/Modules.dox" % (rootPath, pluginName), dictionary)        

    ConfigureFile("%s/TemplatePlugin/__init__.py" % rootForTemplateFiles, "%s/%s/__init__.py" % (rootPath, pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/csnTemplatePlugin.py" % rootForTemplateFiles, "%s/%s/csn%s.py" % (rootPath, pluginName, pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin/TemplatePlugin.cxx" % rootForTemplateFiles, "%s/%s/%s.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePlugin.h" % rootForTemplateFiles, "%s/%s/%s.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginPCH.h" % rootForTemplateFiles, "%s/%s/%sPCH.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginProcessorCollective.cxx" % rootForTemplateFiles, "%s/%s/%sProcessorCollective.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginProcessorCollective.h" % rootForTemplateFiles, "%s/%s/%sProcessorCollective.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginWidgetCollective.cxx" % rootForTemplateFiles, "%s/%s/%sWidgetCollective.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/TemplatePluginWidgetCollective.h" % rootForTemplateFiles, "%s/%s/%sWidgetCollective.h" % (rootPath, pluginName, pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.cxx" % rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.h" % rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.h" % (rootPath, pluginName, pluginName), dictionary)    

    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.cpp" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.cpp" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.h" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.h" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.cpp" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.cpp" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.h" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.h" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.wxg" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.wxg" % (rootPath, pluginName, pluginName, pluginName), dictionary)
    
    # append to toolkit files
    EditFile(tkFilename, "def %s():\n    import Apps.Plugins.%s.csn%s\n    return Apps.Plugins.%s.csn%s.%s"  %(pluginName[0].lower()+pluginName[1:] , pluginName, pluginName, pluginName, pluginName, pluginName[0].lower()+pluginName[1:] ), 1)
    EditFile(gimiasFilename, "%s" % (pluginName[0].lower()+pluginName[1:] ), 2)

def CreatePluginWidget(rootPath, pluginWidgetName, rootForTemplateFiles):
    """ Create a new Widget from template. """
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(pluginWidgetName) == 0:
        raise ValueError("No widget name provided.")
    # plugin name
    pluginName = os.path.basename(rootPath)
    csnFilename = "%s/csn%s.py" % (rootPath, pluginName)
    if not os.path.exists(csnFilename):
        raise IOError("The plugin csnake file does not exist.")

    
    # create dictionary
    dictionary = dict()
    dictionary["Sandbox"] = pluginWidgetName;
    dictionary["sandbox"] = pluginWidgetName[ 0 ].lower( ) + pluginWidgetName[ 1: ];

    # copy template files
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.cxx" % rootForTemplateFiles, "%s/processors/%s%sProcessor.cxx" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.h" % rootForTemplateFiles, "%s/processors/%s%sProcessor.h" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.cpp" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.h" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.cpp" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.h" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.wxg" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.wxg" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)
    
    # append to toolkit files
    EditFile(csnFilename, "%s%sPanelWidget" % (pluginName, pluginWidgetName ), 3)

