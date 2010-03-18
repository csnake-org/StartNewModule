/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _SandboxPluginSubtractProcessor_H
#define _SandboxPluginSubtractProcessor_H

#include "coreProcessorWorkingData.h"

#include "itkImage.h"

namespace SandboxPlugin{

/**
Processor for subtracting two images

\ingroup SandboxPlugin
\author Berta Marti
\date 24 oct 2008
*/
class SubtractProcessor : public Core::FrontEndPlugin::ProcessorWorkingData
{
public:
	//!
	coreDeclareSmartPointerClassMacro(SubtractProcessor, Core::SmartPointerObject);
	typedef itk::Image<float,3> ImageType;
		
	//! Call library to perform operation
	void Update( );

private:
	//!
	SubtractProcessor();

	//!
	~SubtractProcessor();

	//! Purposely not implemented
	SubtractProcessor( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );

private:
	
};
    
} // namespace sdp{

#endif //_SandboxPluginSubtractProcessor_H
