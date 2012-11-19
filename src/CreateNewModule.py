import os.path
import logging

def ConfigureFile(source, dest, dictionary):
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
    for varName in dictionary.keys():
        template = template.replace("%s" % varName, dictionary[varName])
    # create path to dest if not there
    os.path.exists(os.path.dirname(dest)) or os.makedirs(os.path.dirname(dest))
    # write destination file
    f = open(dest, 'w')
    f.write(template)
    f.close()

def CreateDirectory(dest):
    """Create directory in the dest """
    os.path.exists(dest) or os.makedirs(dest)

def EditFile(source, line, typeOption):
    """ Append line to a file according to type."""
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("EditFile: %s" % source)
    # check source file
    if not os.path.exists(source):
        raise IOError("File not found: %s" % source)
    # type 1: main csn file
    if( typeOption == 1) :
        # read file
        f = open(source, 'r')
        content = f.read() 
        f.close()
        # check if line is not already there
        if content.find( line ) == -1:
            f = open(source, 'a')
            f.write("\n%s\n" % line); 
            f.close()
        else:
            logger.warn("The line to insert ('%s') is already present in %s" % (line, source))
    # type 2: gimias csn file
    if( typeOption == 2 ):
        f = open(source, 'r')
        template = f.read() 
        f.close()
        # check if the 'AddProjects' string is present
        if template.find( "AddProjects([" ) == -1:
            raise IOError("Could not find the project group (starting with 'AddProjects(['), \
            are you sure you provided the proper input file?")
        # check if line is not already there
        if template.find( line ) == -1:
            template = template.replace( "AddProjects([", "AddProjects([\n    %s," % line, 1)
            f = open(source, 'w')
            f.write(template)
            f.close()
        else:
            logger.warn("The line to insert ('%s') is already present in %s" % (line, source))
    # type 4: widget collective
    if( typeOption == 4 ):
        f = open(source, 'r')
        template = f.read()
        f.close()
        template = template.replace(".CommandPanel();", ".CommandPanel();\n   Core::Runtime::Kernel::GetGraphicalInterface()->RegisterFactory(\n    %s::Factory::NewBase(), \n    config.Caption(\"%s\").\n    Id(wxID_%s) );\n" % (line,line,line), 1)
        f = open(source, 'w')
        f.write(template)
        f.close()
    # type 5: processor collective
    if( typeOption == 5 ):
        f = open(source, 'r')
        template = f.read()
        f.close()
        template = template.replace("Core::Runtime::Kernel::GetProcessorFactories();", "Core::Runtime::Kernel::GetProcessorFactories();\n    factories->RegisterFactory( %s::Factory::NewBase( ) );\n" % line, 1)
        f = open(source, 'w')
        f.write(template)
        f.close()

def AddWidgetToConfig(fileName, pluginName, widgetName):
    """ Add a widget to a configuration file."""
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("AddWidgetToConfig: %s" % fileName)
    # check source file
    if not os.path.exists(fileName):
        raise IOError("File not found: %s" % fileName)
    # open and read file
    f = open(fileName, 'r')
    template = f.read()
    f.close()
    # instance name
    instanceName = pluginName[ 0 ].lower( ) + pluginName[ 1: ];
    # check if the section is present
    if template.find("widgetModules = [") == -1:
        template = "%s\n%s" % ( template, "# plugin widgets\nwidgetModules = [\n]\n%s.AddWidgetModules(widgetModules, _useQt = 0)" % instanceName)
    # add widget
    if template.find(widgetName) == -1:
        template = template.replace( "widgetModules = [", "widgetModules = [\n  \"%s\"," % widgetName)
    # save file
    f = open(fileName, 'w')
    f.write(template)
    f.close()

def AddProcessorToConfig(fileName, pluginName):
    """ Add a processor to a configuration file."""
    # log
    logger = logging.getLogger("CreateNewModule")
    logger.info("AddProcessorToConfig: %s" % fileName)
    # check source file
    if not os.path.exists(fileName):
        raise IOError("File not found: %s" % fileName)
    # instance name
    instanceName = pluginName[ 0 ].lower( ) + pluginName[ 1: ];
    # open and read file
    f = open(fileName, 'r')
    template = f.read()
    f.close()
    # check if the section is present
    if template.find("AddIncludeFolders") == -1:
        template = "%s\n%s" % ( template, "%s.AddIncludeFolders([])" % instanceName)
    # update file
    template = template.replace("%s.AddIncludeFolders" % instanceName, "%s.AddSources([\"processors/*.cxx\", \"processors/*.h\"])\n%s.AddIncludeFolders" % (instanceName, instanceName))
    template = template.replace("AddIncludeFolders([", "AddIncludeFolders([\"processors\",")
    # save file
    f = open(fileName, 'w')
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
    if not os.path.isfile(tkFilename):
        raise IOError("The toolkit csnake file is not a file.")
    
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

def CreatePlugin(rootPath, pluginName, rootForTemplateFiles, tkFilename, gimiasFilename, gimiasVersion):
    """ Create a new Gimias Plugin from template. """
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
    if not os.path.isfile(tkFilename):
        raise IOError("The toolkit csnake file is not a file.")
    if not os.path.exists(gimiasFilename):
        raise IOError("The gimias csnake file does not exist.")
    if not os.path.isfile(gimiasFilename):
        raise IOError("The gimias csnake file is not a file.")

    # template plugin folder
    templatePluginFolder = "%s/TemplatePlugin%s" % (rootForTemplateFiles, gimiasVersion.replace('.', ''))
    
    # create dictionary
    dictionary = dict()
    dictionary["TemplatePlugin"] = pluginName;
    dictionary["templatePlugin"] = pluginName[ 0 ].lower( ) + pluginName[ 1: ];

    # copy template files
    ConfigureFile("%s/build/config.xml" % templatePluginFolder, "%s/%s/build/config.xml" % (rootPath, pluginName), dictionary)        

    ConfigureFile("%s/tests/templateTest.h" % templatePluginFolder, "%s/%s/tests/templateTest.h" % (rootPath, pluginName), dictionary)
    ConfigureFile("%s/doc/Doxyfile.doxy" % templatePluginFolder, "%s/%s/doc/Doxyfile.doxy" % (rootPath, pluginName), dictionary)        
    ConfigureFile("%s/doc/MainPage.dox" % templatePluginFolder, "%s/%s/doc/MainPage.dox" % (rootPath, pluginName), dictionary)        
    ConfigureFile("%s/doc/Modules.dox" % templatePluginFolder, "%s/%s/doc/Modules.dox" % (rootPath, pluginName), dictionary)        

    ConfigureFile("%s/__init__.py" % templatePluginFolder, "%s/%s/__init__.py" % (rootPath, pluginName), dictionary)
    ConfigureFile("%s/csnTemplatePlugin.py" % templatePluginFolder, "%s/%s/csn%s.py" % (rootPath, pluginName, pluginName), dictionary)
    ConfigureFile("%s/TemplatePlugin.cxx" % templatePluginFolder, "%s/%s/%s.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePlugin.h" % templatePluginFolder, "%s/%s/%s.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePluginPCH.h" % templatePluginFolder, "%s/%s/%sPCH.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePluginProcessorCollective.cxx" % templatePluginFolder, "%s/%s/%sProcessorCollective.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePluginProcessorCollective.h" % templatePluginFolder, "%s/%s/%sProcessorCollective.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePluginWidgetCollective.cxx" % templatePluginFolder, "%s/%s/%sWidgetCollective.cxx" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/TemplatePluginWidgetCollective.h" % templatePluginFolder, "%s/%s/%sWidgetCollective.h" % (rootPath, pluginName, pluginName), dictionary)    
    ConfigureFile("%s/plugin.xml" % templatePluginFolder, "%s/%s/plugin.xml" % (rootPath, pluginName), dictionary)        

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

def CreatePluginWidget(rootPath, pluginWidgetName, rootForTemplateFiles, gimiasVersion):
    """ Create a new Gimias Plugin Widget from template. """
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
    #procCollname = "%s/%sProcessorCollective.cxx" % (rootPath, pluginName)
    #if not os.path.exists(procCollname):
    #    raise IOError("The plugin processor collective file does not exist.")

    # template plugin folder
    templatePluginFolder = "%s/TemplatePlugin%s" % (rootForTemplateFiles, gimiasVersion.replace('.', ''))
    
    # create dictionary
    dictionary = dict()
    dictionary["TemplateWidget"] = pluginWidgetName;
    dictionary["templateWidget"] = pluginWidgetName[ 0 ].lower( ) + pluginWidgetName[ 1: ];
    dictionary["TemplatePlugin"] = pluginName;
    dictionary["templatePlugin"] = pluginName[ 0 ].lower( ) + pluginName[ 1: ];
    
    # copy template files
    ConfigureFile("%s/processors/TemplatePluginTemplateWidgetProcessor.cxx" % templatePluginFolder, "%s/processors/%s%sProcessor.cxx" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/processors/TemplatePluginTemplateWidgetProcessor.h" % templatePluginFolder, "%s/processors/%s%sProcessor.h" % (rootPath, pluginName, pluginWidgetName), dictionary)
    ConfigureFile("%s/widgets/TemplatePluginPanelWidget/TemplatePluginTemplateWidgetPanelWidget.cpp" % templatePluginFolder, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/widgets/TemplatePluginPanelWidget/TemplatePluginTemplateWidgetPanelWidget.h" % templatePluginFolder, "%s/widgets/%s%sPanelWidget/%s%sPanelWidget.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/widgets/TemplatePluginPanelWidget/TemplatePluginTemplateWidgetPanelWidgetUI.cpp" % templatePluginFolder, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.cpp" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/widgets/TemplatePluginPanelWidget/TemplatePluginTemplateWidgetPanelWidgetUI.h" % templatePluginFolder, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.h" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)    
    ConfigureFile("%s/widgets/TemplatePluginPanelWidget/TemplatePluginTemplateWidgetPanelWidgetUI.wxg" % templatePluginFolder, "%s/widgets/%s%sPanelWidget/%s%sPanelWidgetUI.wxg" % (rootPath, pluginName, pluginWidgetName, pluginName, pluginWidgetName), dictionary)
    
    # append to toolkit files
    widgetName = "%s%sPanelWidget" % (pluginName, pluginWidgetName)
    AddWidgetToConfig(csnFilename, pluginName, widgetName)
    AddProcessorToConfig(csnFilename, pluginName)
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
    if not os.path.isfile(tkFilename):
        raise IOError("The toolkit csnake file is not a file.")
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

def CreateCommandLine(rootPath, commandLineName, rootForTemplateFiles):
    """ Create a new CommandLine Plugin from template. """
    # log
    logger = logging.getLogger("CreateCommandLine")
    logger.info("Create CommandLine Plugin.")
    # check inputs
    if len(rootPath) == 0:
        raise ValueError("No root path provided.")
    if len(commandLineName) == 0:
        raise ValueError("No commandline name provided.")

    # create dictionary
    dictionary = dict()
    dictionary["TemplateFilter"] = commandLineName;
    dictionary["templateFilter"] = commandLineName.lower();
    
    #copy template files
    if not os.path.exists("%s/__init__.py" % (rootPath)):
        ConfigureFile("%s/TemplateCLP/__init__.py" % rootForTemplateFiles, "%s/__init__.py" % (rootPath), dictionary)
    ConfigureFile("%s/TemplateCLP/TemplateFilter.cxx" % rootForTemplateFiles, "%s/applications/%s/%s.cxx" % (rootPath, commandLineName,commandLineName),dictionary)
    ConfigureFile("%s/TemplateCLP/TemplateFilter.xml" % rootForTemplateFiles ,"%s/applications/%s/%s.xml" % (rootPath, commandLineName, commandLineName),dictionary)
    ConfigureFile("%s/TemplateCLP/csnTemplateFilter.py" % rootForTemplateFiles ,"%s/csn%s.py" % (rootPath, commandLineName),dictionary)
    