/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePluginTemplateWidgetProcessor_H
#define _TemplatePluginTemplateWidgetProcessor_H

#include "coreBaseProcessor.h"

namespace templatePlugin
{

/**
Processor for ...

\ingroup TemplatePlugin
*/
class TemplateWidgetProcessor : public Core::BaseProcessor
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
	coreProcessor(TemplateWidgetProcessor, Core::BaseProcessor);
	
	//! Call library to perform operation
	void Update( );

private:
	//!
	TemplateWidgetProcessor();

	//!
	~TemplateWidgetProcessor();

	//! Purposely not implemented
	TemplateWidgetProcessor( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );
}; // class TemplateWidgetProcessor
    
} // namespace templatePlugin

#endif //_TemplatePluginTemplateWidgetProcessor_H
