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
        pathToResources = "../resources/"
        pathToSrc = "../src/"
        # Resource files to add to bin folder.
        self.resources = []
        f1 = os.path.join(pathToResources, "about.txt")
        f2 = "resources", [f1]
        self.resources.append(f2)
        f1 = os.path.join(pathToResources, "logging.conf")
        f2 = "resources", [f1]
        self.resources.append(f2)
        # Template code
        folderToParse = ["TemplateLibrary", "TemplatePlugin"]
        for folder in folderToParse:
            for root, dirs, files in os.walk(pathToResources + folder):
                if not root.find( ".svn" ) == -1: # skip svn hidden directories
                    continue
                for name in files:
                    f1 = os.path.join(root, name)
                    f2 = "resources/" + root, [f1]
                    self.resources.append(f2)
        # script file
        self.script = pathToSrc + "StartNewModule.py"
        # options
        about = About()
        about.read( pathToResources + "about.txt")
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
                }
            ],
            data_files = self.resources )

if __name__ == "__main__":
    mainSetup = exeSetup()
    mainSetup.run()
