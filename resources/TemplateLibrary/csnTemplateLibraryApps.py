# CSNake configuration of the Template library applications

# CSNake imports
from csnAPIPublic import GetAPI
api = GetAPI("2.5.0")
# Other dependencies
from csnToolkitOpen import *

# Definition of the template library apps
templateLibraryApps = api.CreateStandardModuleProject("TemplateLibraryApps", "library")
templateLibraryApps.AddSources( [csnUtility.GetDummyCppFilename()] )
templateLibraryApps.AddProjects( [templateLibrary] )
templateLibraryApps.AddApplications([ "tlAppFirst" ], _holderName="TemplateLibraryApplications")
