# Copyright 2007 Pompeu Fabra University (Computational Imaging Laboratory), Barcelona, Spain. Web: www.cilab.upf.edu.
# This software is distributed WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# 

import csnBuild
import csnCilab
import csnUtility
from csnToolkitOpen import *
#from csnToolkitPrivate import *

templateFilterCLP = csnCilab.CommandLinePlugin("TemplateFilterCLP")
templateFilterCLP.AddSources([u'applications/TemplateFilter/TemplateFilter.cxx'])
templateFilterCLP.AddProjects([itk, slicer,generateClp])
#templateFilterCLP.AddDefinitions(["/bigobj"], _private = 1, _WIN32 = 1) 
	
#EveryCLP = csnCilab.CilabModuleProject("templateFilterCLP", "container")
#EveryCLP.AddProjects( [templateFilterCLP] )