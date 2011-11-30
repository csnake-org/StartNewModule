/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePluginProcessorCollective_H
#define _TemplatePluginProcessorCollective_H

#include "coreSmartPointerMacros.h"
#include "coreObject.h"


namespace TemplatePlugin{

/**
This class instantiates all processors used in the plugin and registers them.

\ingroup TemplatePlugin
\author Maarten Nieber
\date 18 jun 2008
*/

class ProcessorCollective : public Core::SmartPointerObject
{
public:
	//!
	coreDeclareSmartPointerClassMacro(ProcessorCollective, Core::SmartPointerObject);

private:
	//! The constructor instantiates all the processors and connects them.
	ProcessorCollective();

};

} // namespace TemplatePlugin{

#endif //_TemplatePluginProcessorCollective_H
