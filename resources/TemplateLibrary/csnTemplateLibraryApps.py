# Used to configure TemplateLibraryApps
import csnCilab
import csnUtility
from csnToolkitOpen import *

templateLibraryApps = csnCilab.CilabModuleProject("TemplateLibraryApps", "library")
templateLibraryApps.AddSources( [csnUtility.GetDummyCppFilename()] )
templateLibraryApps.AddProjects( [templateLibrary] )
templateLibraryApps.AddApplications([ "tlAppFirst" ], _holderName="TemplateLibraryApplications")
