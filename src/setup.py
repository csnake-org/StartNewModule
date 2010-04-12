# Python script used to generate executables.
# Depends on py2exe: http://www.py2exe.org
from distutils.core import setup
import os
# Added options for setup
import py2exe #@UnusedImport

class exeSetup():
    ''' Helper class to generate windows executable.'''
    def __init__(self):
        pathToResources = "../resources/"
        pathToSrc = "../src/"
        # Resource files to add to bin folder.
        self.resources = []
        folderToParse = ["TemplateLibrary", "TemplatePlugin"]
        for folder in folderToParse:
            for root, dirs, files in os.walk(pathToResources + folder):
                if not root.find( ".svn" ) == -1: # skip svn hidden directories
                    continue
                for name in files:
                    f1 = os.path.join(root, name)
                    f2 = "resources/" + root, [f1]
                    self.resources.append(f2)
        # options
        self.name = "StartNewModule"
        self.version = "0.1"
        self.description = "New module/plugin configuration helper."
        self.author = "SSD Team"
        self.script = pathToSrc + "StartNewModule.py"
    
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
