import os.path
import logging

def ConfigureFile(source, dest, dict):
    """ Replace string in source file according to a dictionary. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("ConfigureFile: %s" % dest)
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

def CreateDirectory(dest):
    """Create directory in the dest """
    os.path.exists(dest) or os.makedirs(dest)

def EditFile(source, line, type):
    """ Append line to a file according to type."""
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("EditFile: %s" % source)
    # check source file
    if not os.path.exists(source):
        raise IOError("File not found: %s" % source)
    # type 1: main csn file
    if( type == 1) :
    # read file
        f = open(source, 'r')
        content = f.read() 
        f.close()
        # check if line is not already there
        if content.find( line ) == -1:
            f = open(source, 'a')
            f.write("\n%s\n" % line); 
            f.close()
    # type 2: gimias csn file
    if( type == 2 ):
        f = open(source, 'r')
        template = f.read() 
        f.close()
        # check if line is not already there
        if template.find( line ) == -1:
            template = template.replace( "AddProjects([", "AddProjects([\n    %s," % line)
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
    # type 4: widget collective
    if( type == 4 ):
        f = open(source, 'r')
        template = f.read()
        f.close()
        template = template.replace(".CommandPanel();", ".CommandPanel();\n   Core::Runtime::Kernel::GetGraphicalInterface()->RegisterFactory(\n    %s::Factory::NewBase(), \n    config.Caption(\"%s\").\n    Id(wxID_%s) );\n" % (line,line,line))
        f = open(source, 'w')
        f.write(template)
        f.close()
    # type 5: processor collective
    if( type == 5 ):
        f = open(source, 'r')
        template = f.read()
        f.close()
        template = template.replace("Core::Runtime::Kernel::GetProcessorFactories();", "Core::Runtime::Kernel::GetProcessorFactories();\n    factories->RegisterFactory( %s::Factory::NewBase( ) );\n" % line)
        f = open(source, 'w')
        f.write(template)
        f.close()

def AddHeaderFile(source, line1, line2):
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("AddHeaderFile: %s" % source)
    # replace line1 with line1 \n line2
    f = open(source, 'r')
    template = f.read()
    f.close()
    template = template.replace(line1,"%s\n%s" % (line1,line2))
    f = open(source, 'w')
    f.write(template)
    f.close()

def CreateLibrary(rootPath, libraryName, rootForTemplateFiles, tkFilename):
    """ Create a new Library from template. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("Create Library.")
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
    
    pathToLib = ""
    ( head , tail ) =os.path.split(rootPath)
    while not os.path.exists(os.path.join(head,os.path.basename(tkFilename))):
        pathToLib = tail +"." +  pathToLib
        ( head , tail ) =os.path.split(head)
   
    if os.path.exists(os.path.join(head,os.path.basename(tkFilename))):
        pathToLib = tail + "." + pathToLib
    # append to toolkit file
    EditFile(tkFilename, "def %s():\n    import %s%s.csn%s\n    return %s%s.csn%s.%s" %(libraryName[0].lower()+libraryName[1:], pathToLib, libraryName, libraryName, pathToLib, libraryName, libraryName, libraryName[0].lower()+libraryName[1:]), 1)
    ( tkFilenameBase, tail) = os.path.splitext(os.path.basename(tkFilename))
    libraryAppsCsnFile = "%s/%s/csn%sApps.py" % (rootPath, libraryName, libraryName)
    if not tkFilenameBase == "csnToolkitOpen" :
        AddHeaderFile(libraryAppsCsnFile,"from csnToolkitOpen import *", "from %s import * \n" % tkFilenameBase )

def CreatePlugin(rootPath, pluginName, rootForTemplateFiles, tkFilename, gimiasFilename):
    """ Create a new Plugin from template. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("Create Plugin.")
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

    ConfigureFile("%s/TemplatePlugin/tests/templateTest.h" % rootForTemplateFiles, "%s/%s/tests/templateTest.h" % (rootPath, pluginName), dictionary)
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
    ConfigureFile("%s/TemplatePlugin/plugin.xml" % rootForTemplateFiles, "%s/%s/config.xml" % (rootPath, pluginName), dictionary)        

    #ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.cxx" % rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    #ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginSandboxProcessor.h" % rootForTemplateFiles, "%s/%s/processors/%sSandboxProcessor.h" % (rootPath, pluginName, pluginName), dictionary)    

    #ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.cpp" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.cpp" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    #ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidget.h" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidget.h" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    #ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.cpp" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.cpp" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    #ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.h" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.h" % (rootPath, pluginName, pluginName, pluginName), dictionary)    
    #ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginSandboxPanelWidgetUI.wxg" % rootForTemplateFiles, "%s/%s/widgets/%sSandboxPanelWidget/%sSandboxPanelWidgetUI.wxg" % (rootPath, pluginName, pluginName, pluginName), dictionary)
    
    pathToPlugin = ""
    ( head , tail ) =os.path.split(rootPath)
    while not os.path.exists(os.path.join(head,os.path.basename(tkFilename))):
        pathToPlugin = tail +"." +  pathToPlugin
        ( head , tail ) =os.path.split(head)
    
    if os.path.exists(os.path.join(head,os.path.basename(tkFilename))):
        pathToPlugin = tail + "." + pathToPlugin
    
    # append to toolkit files
    EditFile(tkFilename, "def %s():\n    import %s%s.csn%s\n    return %s%s.csn%s.%s"  %(pluginName[0].lower()+pluginName[1:] , pathToPlugin, pluginName, pluginName, pathToPlugin ,pluginName, pluginName, pluginName[0].lower()+pluginName[1:] ), 1)
    EditFile(gimiasFilename, "%s" % (pluginName[0].lower()+pluginName[1:] ), 2)
    # append csnToolkit to csnPlugin
    plugincsnFile = "%s/%s/csn%s.py" % (rootPath,pluginName,pluginName) 
    ( tkFilenameBase , ext ) = os.path.splitext(os.path.basename(tkFilename))
    if not os.path.basename(tkFilename) == "csnGIMIASDef.py" :
        AddHeaderFile(plugincsnFile,"from csnGIMIASDef import *", "from %s import * \n" % tkFilenameBase )

def CreatePluginWidget(rootPath, pluginWidgetName, rootForTemplateFiles):
    """ Create a new Widget from template. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("Create Plugin Widget.")
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
    widgetCollname = "%s/%sWidgetCollective.cxx" % (rootPath, pluginName)
    if not os.path.exists(widgetCollname):
        raise IOError("The plugin widget collective file does not exist.")
    procCollname = "%s/%sProcessorCollective.cxx" % (rootPath, pluginName)
    if not os.path.exists(procCollname):
        raise IOError("The plugin processor collective file does not exist.")

    
    # create dictionary
    dictionary = dict()
    dictionary["Templ"] = pluginWidgetName;
    dictionary["templ"] = pluginWidgetName[ 0 ].lower( ) + pluginWidgetName[ 1: ];
    dictionary["TemplatePlugin"] = pluginName;
    
    # copy template files
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginTemplProcessor.cxx" % rootForTemplateFiles, "%s/processors/%s%sProcessor.cxx" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/processors/TemplatePluginTemplProcessor.h" % rootForTemplateFiles, "%s/processors/%s%sProcessor.h" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginTemplPanelWidget.cpp" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginTemplPanelWidget.h" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginTemplPanelWidgetUI.cpp" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginTemplPanelWidgetUI.h" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/TemplatePlugin/widgets/TemplatePluginPanelWidget/TemplatePluginTemplPanelWidgetUI.wxg" % rootForTemplateFiles, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.wxg" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)
    
    # append to toolkit files
    EditFile(csnFilename, "%s%sPanelWidget" % (pluginName, pluginWidgetName ), 3)
    # append to WidgetCollective 
    EditFile(widgetCollname,"%sPanelWidget" % pluginWidgetName ,4)
    AddHeaderFile(widgetCollname,"#include \"%sWidgetCollective.h\"" % pluginName , "#include \"%s%sPanelWidget.h\"\nconst long wxID_%sPanelWidget = wxNewId();\n" % (pluginName,pluginWidgetName,pluginWidgetName) )
    # append to ProcessorCollective
    #EditFile(procCollname, "%s::%sProcessor" % (pluginName, pluginWidgetName ),5)
    #AddHeaderFile(procCollname,"#include \"%sProcessorCollective.h\"" % pluginName , "#include \"%s%sProcessor.h\"\n" % (pluginName,pluginWidgetName) )

def CreateThirdParty(rootPath, thirdPartyName, rootForTemplateFiles, tkFilename):
    """ Create a new ThirdParty from template. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("Create ThirdParty.")
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(thirdPartyName) == 0:
        raise ValueError("No thirdparty name provided.")
    if not os.path.exists(tkFilename):
        raise IOError("The toolkit csnake file does not exist.")
    cmakeFileName = os.path.join(rootPath ,"CMakeLists.txt")
    if not os.path.exists(cmakeFileName):
        raise IOError("The CMakeLists file does not exist.")

    # create dictionary
    dictionary = dict()
    dictionary["TemplateThirdParty"] = thirdPartyName;
    dictionary["templateThirdParty"] = thirdPartyName.lower( );
    
    # copy template files
    ConfigureFile("%s/TemplateThirdParty/csnTemplateThirdParty.py" % rootForTemplateFiles, "%s/%s/csn%s.py" % (rootPath,thirdPartyName,thirdPartyName), dictionary)
    ConfigureFile("%s/TemplateThirdParty/UseTemplateThirdParty.cmake.in" % rootForTemplateFiles, "%s/%s/Use%s.cmake.in" % (rootPath,thirdPartyName,thirdPartyName), dictionary)
    ConfigureFile("%s/TemplateThirdParty/TemplateThirdPartyConfig.cmake.in" % rootForTemplateFiles, "%s/%s/%sConfig.cmake.in" % (rootPath,thirdPartyName,thirdPartyName), dictionary)
    ConfigureFile("%s/TemplateThirdParty/CMakeLists.txt" % rootForTemplateFiles, "%s/%s/CMakeLists.txt" % (rootPath,thirdPartyName), dictionary)
    ConfigureFile("%s/TemplateThirdParty/__init__.py" % rootForTemplateFiles, "%s/%s/__init__.py" % (rootPath,thirdPartyName), dictionary)
    CreateDirectory("%s/%s/lib" % (rootPath,thirdPartyName))
    CreateDirectory("%s/%s/include" % (rootPath,thirdPartyName))
    
    # append to toolkit files
    EditFile(tkFilename, "\ndef %s():\n    return csnCilab.LoadThirdPartyModule( '%s', 'csn%s').%s\n"  %(thirdPartyName.lower(), thirdPartyName,thirdPartyName ,thirdPartyName.lower()), 1)
    
    # append to CMakeLists.txt de thirdParty folder
    AddHeaderFile(cmakeFileName,"# Set the folder of the thirdparty project", "LIST( APPEND AVAILABLE_THIRDPARTY \"%s\" )\n" % thirdPartyName)

def CreateProject(rootPath, projectName, rootForTemplateFiles):
    """ Create a new Project from Template. """
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("CreateProject")
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(projectName) == 0:
        raise ValueError("No project name provided")

    # create dictionary
    dictionary = dict()
    dictionary["TemplateProject"] = projectName;
    dictionary["templateproject"] = projectName.lower();

    #copy template files
    ConfigureFile("%s/TemplateProject/data/__init__.py" % rootForTemplateFiles, "%s/%s/data/__init__.py" % (rootPath, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/__init__.py" % rootForTemplateFiles ,"%s/%s/%s_src/__init__.py" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/rootFolder.csnake" % rootForTemplateFiles ,"%s/%s/%s_src/rootFolder.csnake" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/modules/__init__.py" % rootForTemplateFiles ,"%s/%s/%s_src/modules/__init__.py" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/plugins/__init__.py" % rootForTemplateFiles ,"%s/%s/%s_src/plugins/__init__.py" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/__init__.py" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/__init__.py" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/CMakeLists.txt" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/CMakeLists.txt" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/cmakeMacros/PCHSupport_26.cmake" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/cmakeMacros/PCHSupport_26.cmake" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/cmakeMacros/PlatformDependent.cmake" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/cmakeMacros/PlatformDependent.cmake" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/cmakeMacros/ResetCachedValues.cmake" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/cmakeMacros/ResetCachedValues.cmake" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/thirdparties/cmakeMacros/ThirdPartyLibMacros.cmake" % rootForTemplateFiles ,"%s/%s/%s_src/thirdparties/cmakeMacros/ThirdPartyLibMacros.cmake" % (rootPath, projectName, projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/csnTemplateProject.py" % rootForTemplateFiles ,"%s/%s/%s_src/csn%s.py" % (rootPath, projectName, projectName,projectName),dictionary)
    ConfigureFile("%s/TemplateProject/TemplateProject_src/csnTemplateProjectToolkit.py" % rootForTemplateFiles ,"%s/%s/%s_src/csn%sToolkit.py" % (rootPath, projectName, projectName,projectName),dictionary)
