/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _TemplatePluginWidgetCollective_H
#define _TemplatePluginWidgetCollective_H

#include "coreFrontEndPlugin.h"
#include "coreSmartPointerMacros.h"
#include "coreObject.h"
#include "coreWidgetCollective.h"

#include "TemplatePluginProcessorCollective.h"

namespace TemplatePlugin{

class SandboxPanelWidget;

/**
This class instantiates all widgets used in the plugin. The widgets are used to operate the plugin processors
(see ProcessorCollective).
In the TemplatePlugin, there is currently only one widget, but when the number of widgets grows, this class
ensures that the code remains maintainable.

\ingroup TemplatePlugin
\author Maarten Nieber
\date 18 jun 2008
*/

class WidgetCollective : public Core::WidgetCollective
{
public:
	//!
	coreDeclareSmartPointerClassMacro(
		WidgetCollective, 
		Core::WidgetCollective );

	/** The constructor instantiates all the widgets and connects them to 
	the processors.
	It is private because clients must use the New function, which returns 
	a smart pointer, to instantiate this class.
	*/
	void Init(
		TemplatePlugin::ProcessorCollective::Pointer processors, 
		Core::FrontEndPlugin::FrontEndPlugin::Pointer frontEndPlugin);

private:
	WidgetCollective( );

	//! 
	void EnablePluginTabWidgets();

	//! See m_ShapeScalePanelWidget.
	void CreateSandboxPanelWidget();

private:

	//! 
	ProcessorCollective::Pointer m_Processors;

	//! Holds the widget for mesh editing
	SandboxPanelWidget* m_SandboxPanelWidget;

};

} // namespace TemplatePlugin

#endif //_TemplatePluginWidgetCollective_H
