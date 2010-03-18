/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginProcessorCollective.h"

SandboxPlugin::ProcessorCollective::ProcessorCollective()
{
	m_ShapeScaleProcessor = ShapeScaleProcessor::New( );
	m_SubtractProcessor = SubtractProcessor::New( );
	m_ResampleProcessor = ResampleProcessor::New( );
}

SandboxPlugin::ShapeScaleProcessor::Pointer 
SandboxPlugin::ProcessorCollective::GetShapeScaleProcessor() const
{
	return m_ShapeScaleProcessor;
}

SandboxPlugin::SubtractProcessor::Pointer 
SandboxPlugin::ProcessorCollective::GetSubtractProcessor() const
{
	return m_SubtractProcessor;
}

SandboxPlugin::ResampleProcessor::Pointer 
SandboxPlugin::ProcessorCollective::GetResampleProcessor() const
{
	return m_ResampleProcessor;
}
