/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePlugin_H
#define _TemplatePlugin_H

#include "TemplatePluginProcessorCollective.h"
#include "TemplatePluginWidgetCollective.h"

// CoreLib
#include "coreFrontEndPlugin.h"

namespace TemplatePlugin{

/** 
\brief Creates all objects of the plug-in and connect them.

\note Nobody can get access to this class. This class is only for 
initialization of all components. 

\note Try to make all processors reusable for other plug-ins. Be aware 
of creating a dependency between the processor and any class of the rest 
of the plug-in.

\ingroup TemplatePlugin
\author Jakub Lyko
\date 07 April 2008
*/
class PLUGIN_EXPORT TemplatePlugin : public Core::FrontEndPlugin::FrontEndPlugin
{
// TYPE DEFINITIONS
public:
	coreDeclareSmartPointerClassMacro(TemplatePlugin, Core::FrontEndPlugin::FrontEndPlugin);

// OPERATIONS
protected:
	//!
	TemplatePlugin(void);

	//!
	virtual ~TemplatePlugin(void);

private:
	//! Purposely not implemented
	TemplatePlugin( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );

private:
	//! Contains all the processors for the plugin
	ProcessorCollective::Pointer m_Processors;

	//! Contains all the widgets for the plugin
	WidgetCollective::Pointer m_Widgets;
};

} // namespace TemplatePlugin

#endif // TemplatePlugin_H
