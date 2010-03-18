/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginWidgetCollective.h"
#include "SandboxPluginShapeScalePanelWidget.h"
#include "SandboxPluginSubtractPanelWidget.h"
#include "SandboxPluginResamplePanelWidget.h"

#include "wxID.h"

#include "coreFrontEndPlugin.h"
#include "corePluginTab.h"

const long wxID_ShapeScalePanelWidget = wxNewId( );
const long wxID_SubtractPanelWidget = wxNewId( );
const long wxID_ResamplePanelWidget = wxNewId( );

SandboxPlugin::WidgetCollective::WidgetCollective( ) 
{
}

void SandboxPlugin::WidgetCollective::Init( 
	SandboxPlugin::ProcessorCollective::Pointer processors, 
	Core::FrontEndPlugin::FrontEndPlugin::Pointer frontEndPlugin )
{
	Superclass::Init( frontEndPlugin );

	m_Processors = processors;

	// Panel widgets
	CreateShapeScalePanelWidget();
	CreateSubtractPanelWidget( );
	CreateResamplePanelWidget( );
}

void SandboxPlugin::WidgetCollective::EnablePluginTabWidgets()
{
	Superclass::EnablePluginTabWidgets();
}

void SandboxPlugin::WidgetCollective::CreateShapeScalePanelWidget()
{
	m_ShapeScalePanelWidget = new SandboxPlugin::ShapeScalePanelWidget(
		m_FrontEndPlugin->GetPluginTab(), 
		wxID_ShapeScalePanelWidget);
	m_ShapeScalePanelWidget->Init( 
		m_Processors->GetShapeScaleProcessor(),
		m_FrontEndPlugin->GetGUIDataContainer()->GetRenderingTree(),
		m_FrontEndPlugin->GetPluginTab()->GetDataEntityListBrowser(),
		m_FrontEndPlugin->GetPluginTab()->GetUserHelperWidget( ) );
	m_FrontEndPlugin->GetPluginTab()->AddWidgetToCommandPanel(
		m_ShapeScalePanelWidget, 
		m_ShapeScalePanelWidget->GetLabel().c_str());
}

void SandboxPlugin::WidgetCollective::CreateSubtractPanelWidget()
{
	m_SubtractPanelWidget = new SandboxPlugin::SubtractPanelWidget(
		m_FrontEndPlugin->GetPluginTab(), 
		wxID_SubtractPanelWidget);
	m_SubtractPanelWidget->Init( 
		m_Processors->GetSubtractProcessor(),
		m_FrontEndPlugin->GetGUIDataContainer()->GetRenderingTree(),
		m_FrontEndPlugin->GetPluginTab()->GetDataEntityListBrowser(),
		m_FrontEndPlugin->GetPluginTab()->GetUserHelperWidget( ) );
	m_FrontEndPlugin->GetPluginTab()->AddWidgetToCommandPanel(
		m_SubtractPanelWidget, 
		m_SubtractPanelWidget->GetLabel().c_str() );
}

void SandboxPlugin::WidgetCollective::CreateResamplePanelWidget()
{
	m_ResamplePanelWidget = new SandboxPlugin::ResamplePanelWidget(
		m_FrontEndPlugin->GetPluginTab(), 
		wxID_ResamplePanelWidget);
	m_ResamplePanelWidget->Init( 
		m_Processors->GetResampleProcessor(),
		m_FrontEndPlugin->GetGUIDataContainer()->GetRenderingTree(),
		m_FrontEndPlugin->GetPluginTab()->GetDataEntityListBrowser(),
		m_FrontEndPlugin->GetPluginTab()->GetUserHelperWidget( ) );
	m_FrontEndPlugin->GetPluginTab()->AddWidgetToCommandPanel(
		m_ResamplePanelWidget, 
		m_ResamplePanelWidget->GetLabel().c_str() );
}

