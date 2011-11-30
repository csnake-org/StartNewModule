/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePluginTemplProcessor_H
#define _TemplatePluginTemplProcessor_H

#include "coreBaseProcessor.h"
#include "coreProcessorFactory.h"

namespace TemplatePlugin{

/**
Processor for 

\ingroup TemplatePlugin
\author Xavi Planes
\date 16 feb 2009
*/
class TemplProcessor : public Core::BaseProcessor
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
		OUTPUT_2,
		OUTPUTS_NUMBER
	}OUTPUT_TYPE;
public:
	//!
	coreProcessor(TemplProcessor, Core::BaseProcessor);
	
	//! Call library to perform operation
	void Update( );

private:
	//!
	TemplProcessor();

	//!
	~TemplProcessor();

	//! Purposely not implemented
	TemplProcessor( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );
};
    
} // namespace TemplatePlugin{

#endif //_TemplatePluginTemplProcessor_H
