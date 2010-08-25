# Python script used to generate executables.
# Depends on py2exe: http://www.py2exe.org
from distutils.core import setup
import os
# Added options for setup
import py2exe #@UnusedImport
from about import About

class exeSetup():
    ''' Helper class to generate windows executable.'''
    def __init__(self):
        pathToResources = "../resources"
        pathToSrc = "../src"
        # Resources of the setup script
        self.resources = []
        # Resource files to add to bin folder.
        self.__addToResources(pathToResources)
        # Doc files to add to bin folder.
        self.__addToResources("../doc/html")
        # script file
        self.script = pathToSrc + "/StartNewModule.py"
        self.icon_resource = pathToResources + "/startnewmodule.ico"
        # options
        about = About()
        about.read( pathToResources + "/about.txt")
        self.name = about.getName()
        self.version = about.getVersion()
        self.description = about.getDescription()
        self.author = about.getAuthor()
    
    def run(self):
        ''' Run the setup. '''
        setup(
            name=self.name,
            version=self.version,
            description=self.description,
            author=self.author,
            windows=[ 
                {
                    "script": self.script,
                    "icon_resources": [(1, self.icon_resource)]
                }
            ],
            data_files = self.resources )

    def __addToResources(self, origin):
        for root, dirs, files in os.walk(origin):
            if not root.find( ".svn" ) == -1: # skip svn hidden directories
                continue
            for name in files:
                f1 = os.path.join(root, name)
                f2 = "dist/" + root, [f1]
                self.resources.append(f2)

if __name__ == "__main__":
    mainSetup = exeSetup()
    mainSetup.run()
