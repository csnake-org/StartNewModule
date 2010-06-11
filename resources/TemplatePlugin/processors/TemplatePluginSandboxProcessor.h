/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePluginSandboxProcessor_H
#define _TemplatePluginSandboxProcessor_H

#include "coreBaseProcessor.h"
#include "coreProcessorFactory.h"

namespace TemplatePlugin{

/**
Processor for 

\ingroup TemplatePlugin
\author Xavi Planes
\date 16 feb 2009
*/
class SandboxProcessor : public Core::BaseProcessor
{
public:

	typedef itk::Image<float,3> ImageType;

	typedef enum
	{
		INPUT_0,
		INPUT_1,
		INPUTS_NUMBER
	} INPUT_TYPE;

	typedef enum
	{
		OUTPUT_0,
		OUTPUT_1,
		OUTPUTS_NUMBER
	}OUTPUT_TYPE;
public:
	//!
	coreProcessor(SandboxProcessor, Core::BaseProcessor);
	
	//! Call library to perform operation
	void Update( );

private:
	//!
	SandboxProcessor();

	//!
	~SandboxProcessor();

	//! Purposely not implemented
	SandboxProcessor( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );
};
    
} // namespace TemplatePlugin{

#endif //_TemplatePluginSandboxProcessor_H
