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

#include "TemplatePluginSandboxProcessor.h"

namespace TemplatePlugin{

/**
This class instantiates all processors used in the plugin.
In the TemplatePlugin, there is currently only one processor. Normally, 
you would not create a separate class to store only one processor. However, 
a real plugin has many processors that are usually connected: the output of
one processor is the input for another processor. The responsibility of the 
ProcessorCollective is to instantiate all these processors and connect them 
in the right way.

\ingroup TemplatePlugin
\author Maarten Nieber
\date 18 jun 2008
*/

class ProcessorCollective : public Core::SmartPointerObject
{
public:
	//!
	coreDeclareSmartPointerClassMacro(ProcessorCollective, Core::SmartPointerObject);

	//!
	SandboxProcessor::Pointer GetSandboxProcessor() const;


private:
	//! The constructor instantiates all the processors and connects them.
	ProcessorCollective();

private:
	//! Holds the processor.
	SandboxProcessor::Pointer m_SandboxProcessor;
};

} // namespace TemplatePlugin{

#endif //_TemplatePluginProcessorCollective_H
