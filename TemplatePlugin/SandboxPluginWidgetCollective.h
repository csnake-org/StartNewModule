/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _SandboxPluginWidgetCollective_H
#define _SandboxPluginWidgetCollective_H

#include "coreFrontEndPlugin.h"
#include "coreSmartPointerMacros.h"
#include "coreObject.h"
#include "coreWidgetCollective.h"

#include "SandboxPluginProcessorCollective.h"

namespace SandboxPlugin{

class SubtractPanelWidget;
class ShapeScalePanelWidget;
class ResamplePanelWidget;

/**
This class instantiates all widgets used in the plugin. The widgets are used to operate the plugin processors
(see ProcessorCollective).
In the SandboxPlugin, there is currently only one widget, but when the number of widgets grows, this class
ensures that the code remains maintainable.

\ingroup SandboxPlugin
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
		SandboxPlugin::ProcessorCollective::Pointer processors, 
		Core::FrontEndPlugin::FrontEndPlugin::Pointer frontEndPlugin);

private:
	WidgetCollective( );

	//! 
	void EnablePluginTabWidgets();

	//! See m_ShapeScalePanelWidget.
	void CreateShapeScalePanelWidget();

	//! See m_SubtractPanelWidget.
	void CreateSubtractPanelWidget();

	//! See m_ResamplePanelWidget.
	void CreateResamplePanelWidget();

private:

	//! 
	ProcessorCollective::Pointer m_Processors;

	//! Holds the widget for mesh editing
	ShapeScalePanelWidget* m_ShapeScalePanelWidget;

	//! Holds the widget for subtract images
	SubtractPanelWidget* m_SubtractPanelWidget;

	//! Holds the widget for resampling an image
	ResamplePanelWidget* m_ResamplePanelWidget;
};

} // namespace SandboxPlugin

#endif //_SandboxPluginWidgetCollective_H
