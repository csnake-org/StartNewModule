/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _SandboxPluginProcessorCollective_H
#define _SandboxPluginProcessorCollective_H

#include "coreSmartPointerMacros.h"
#include "coreObject.h"

#include "SandboxPluginShapeScaleProcessor.h"
#include "SandboxPluginSubtractProcessor.h"
#include "SandboxPluginResampleProcessor.h"

namespace SandboxPlugin{

/**
This class instantiates all processors used in the plugin.
In the SandboxPlugin, there is currently only one processor. Normally, 
you would not create a separate class to store only one processor. However, 
a real plugin has many processors that are usually connected: the output of
one processor is the input for another processor. The responsibility of the 
ProcessorCollective is to instantiate all these processors and connect them 
in the right way.

\ingroup SandboxPlugin
\author Maarten Nieber
\date 18 jun 2008
*/

class ProcessorCollective : public Core::SmartPointerObject
{
public:
	//!
	coreDeclareSmartPointerClassMacro(ProcessorCollective, Core::SmartPointerObject);

	//!
	ShapeScaleProcessor::Pointer GetShapeScaleProcessor() const;

	//!
	SubtractProcessor::Pointer GetSubtractProcessor() const;

	//!
	ResampleProcessor::Pointer GetResampleProcessor() const;

private:
	//! The constructor instantiates all the processors and connects them.
	ProcessorCollective();

private:
	//! Holds the processor for mesh editing.
	ShapeScaleProcessor::Pointer m_ShapeScaleProcessor;

	//! Holds the processor for subtract images
	SubtractProcessor::Pointer m_SubtractProcessor;

	//! Holds the processor for resample image
	ResampleProcessor::Pointer m_ResampleProcessor;
};

} // namespace SandboxPlugin{

#endif //_SandboxPluginProcessorCollective_H
