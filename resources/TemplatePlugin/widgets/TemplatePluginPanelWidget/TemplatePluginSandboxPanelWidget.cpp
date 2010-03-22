/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "TemplatePluginSandboxPanelWidget.h"

// GuiBridgeLib
#include "gblWxBridgeLib.h"
#include "gblWxButtonEventProxy.h"
// Core
#include "coreDataEntityHelper.h"
#include "coreUserHelperWidget.h"

// Core
#include "coreAcquireDataEntityInputControl.h"
#include "coreDataTreeHelper.h"
#include "coreDataEntityListBrowser.h"
#include "coreReportExceptionMacros.h"
#include "coreProcessorWidgetsBuilder.h"


TemplatePlugin::SandboxPanelWidget::SandboxPanelWidget( wxWindow* parent, int id )
: TemplatePluginSandboxPanelWidgetUI(parent, id)
{
	SetLabel( "SandboxPanelWidget" );
}

TemplatePlugin::SandboxPanelWidget::~SandboxPanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void TemplatePlugin::SandboxPanelWidget::Init( 
	TemplatePlugin::SandboxProcessor::Pointer processor,
	Core::RenderingTree::Pointer tree,
	Core::Widgets::DataEntityListBrowser* listBrowser,
	Core::Widgets::UserHelper *helperWidget )
{
	//------------------------------------------------------
	m_Processor = processor;
	m_RenderingTree = tree;
	m_helperWidget = helperWidget;
	m_selectedDataEntityHolder = listBrowser->GetSelectedDataEntityHolder();


	Core::ProcessorWidgetsBuilder::Init( m_Processor.GetPointer(), this, listBrowser, true );

	//------------------------------------------------------
	// Observers to data
	m_Processor->GetOutputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&SandboxPanelWidget::OnModifiedOutputDataEntity );

	m_Processor->GetInputDataEntityHolder( SandboxProcessor::INPUT_0 )->AddObserver( 
		this, 
		&SandboxPanelWidget::OnModifiedInputDataEntity );


	UpdateWidget();
}

void TemplatePlugin::SandboxPanelWidget::UpdateWidget()
{
	
	UpdateHelperWidget( );

	Validate();
}

void TemplatePlugin::SandboxPanelWidget::UpdateData()
{
	if( !Validate() )
		return;
	// Set parameters to processor. Pending
}

bool TemplatePlugin::SandboxPanelWidget::Validate()
{
	bool okay = true;

	// Validate each text control. Pending
	return okay;
}


void TemplatePlugin::SandboxPanelWidget::OnBtnApply(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		// Update the scale values from widget to processor
		UpdateData();

		m_Processor->Update( );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "SandboxPanelWidget::OnBtnApply" );
}


void TemplatePlugin::SandboxPanelWidget::OnModifiedOutputDataEntity()
{
	try{

		Core::DataEntity::Pointer inputDataEntity;
		inputDataEntity = m_Processor->GetInputDataEntity( SandboxProcessor::INPUT_0 );

		// Hide input if is different from output and output is not empty
		if ( m_Processor->GetOutputDataEntity( 0 ).IsNotNull() && 
			 m_Processor->GetOutputDataEntity( 0 ) != inputDataEntity )
		{
			m_RenderingTree->Show( inputDataEntity, false );
		}

		// Add output to the data list and render it
		// After adding the output, the input will automatically be changed to
		// this one
		Core::DataTreeHelper::PublishOutput( 
			m_Processor->GetOutputDataEntityHolder( 0 ), 
			m_RenderingTree,
			m_selectedDataEntityHolder );
	
	}
	coreCatchExceptionsLogAndNoThrowMacro( 
		"CardiacInitializationPanelWidget::OnModifiedOutputDataEntity")

}

void TemplatePlugin::SandboxPanelWidget::UpdateHelperWidget()
{
		m_helperWidget->SetInfo( 
			Core::Widgets::HELPER_INFO_LEFT_BUTTON, 
			" info that is useful in order to use the processor" );

}

bool TemplatePlugin::SandboxPanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = TemplatePluginSandboxPanelWidgetUI::Enable( enable );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void TemplatePlugin::SandboxPanelWidget::OnModifiedInputDataEntity()
{
	UpdateWidget();
}
