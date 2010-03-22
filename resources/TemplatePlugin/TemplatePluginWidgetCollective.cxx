/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "TemplatePluginWidgetCollective.h"
#include "TemplatePluginSandboxPanelWidget.h"

#include "wxID.h"

#include "coreFrontEndPlugin.h"
#include "corePluginTab.h"

const long wxID_SandboxPanelWidget = wxNewId( );

TemplatePlugin::WidgetCollective::WidgetCollective( ) 
{
}

void TemplatePlugin::WidgetCollective::Init( 
	TemplatePlugin::ProcessorCollective::Pointer processors, 
	Core::FrontEndPlugin::FrontEndPlugin::Pointer frontEndPlugin )
{
	Superclass::Init( frontEndPlugin );

	m_Processors = processors;

	// Panel widgets
	CreateSandboxPanelWidget();
}

void TemplatePlugin::WidgetCollective::EnablePluginTabWidgets()
{
	Superclass::EnablePluginTabWidgets();
}

void TemplatePlugin::WidgetCollective::CreateSandboxPanelWidget()
{
	m_SandboxPanelWidget = new TemplatePlugin::SandboxPanelWidget(
		m_FrontEndPlugin->GetPluginTab(), 
		wxID_SandboxPanelWidget);
	m_SandboxPanelWidget->Init( 
		m_Processors->GetSandboxProcessor(),
		m_FrontEndPlugin->GetGUIDataContainer()->GetRenderingTree(),
		m_FrontEndPlugin->GetPluginTab()->GetDataEntityListBrowser(),
		m_FrontEndPlugin->GetPluginTab()->GetUserHelperWidget( ) );
	m_FrontEndPlugin->GetPluginTab()->AddWidgetToCommandPanel(
		m_SandboxPanelWidget, 
		m_SandboxPanelWidget->GetLabel().c_str());
}
