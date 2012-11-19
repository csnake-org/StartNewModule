# CSNake configuration of the Template filters

# CSNake imports
from csnAPIPublic import GetAPI
api = GetAPI("2.5.0")
# Other dependencies
from csnToolkitOpen import *
#from csnGIMIASDef import *

# Definition of the templateFilter CLP
templateFilterCLP = CommandLinePlugin("TemplateFilterCLP")
templateFilterCLP.AddSources([u'applications/TemplateFilter/TemplateFilter.cxx'])
templateFilterCLP.AddProjects([itk, slicer, generateClp])
	
# Contained for all the CLP of this file
#everyCLP = api.CreateStandardModuleProject("templateFilterCLP", "container")
#everyCLP.AddProjects([templateFilterCLP])
