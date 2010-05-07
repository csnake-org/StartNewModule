# Used to configure TemplateLibraryApps

import csnBuild
import csnCilab
import csnUtility
import csnTemplateLibrary
from csnCISTIBToolkit import *

templateLibraryApps = csnCilab.CilabModuleProject("TemplateLibraryApps", "library")
templateLibraryApps.AddSources( [csnUtility.GetDummyCppFilename()] )
templateLibraryApps.AddProjects( [csnTemplateLibrary.templateLibrary] )
templateLibraryApps.AddApplications([ "tlAppFirst" ], _holderName="TemplateLibraryApplications")
