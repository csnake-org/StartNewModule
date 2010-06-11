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
#include "coreDataTreeHelper.h"
#include "coreReportExceptionMacros.h"


TemplatePlugin::SandboxPanelWidget::SandboxPanelWidget(  wxWindow* parent, int id/*= wxID_ANY*/,
													   const wxPoint&  pos /*= wxDefaultPosition*/, 
													   const wxSize&  size /*= wxDefaultSize*/, 
													   long style/* = 0*/ )
: TemplatePluginSandboxPanelWidgetUI(parent, id,pos,size,style)
{
	m_Processor = TemplatePlugin::SandboxProcessor::New();

	SetName( "Sandbox Panel Widget" );
}

TemplatePlugin::SandboxPanelWidget::~SandboxPanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void TemplatePlugin::SandboxPanelWidget::OnInit( )
{
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

}

void TemplatePlugin::SandboxPanelWidget::UpdateData()
{
	// Set parameters to processor. Pending
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
			GetRenderingTree( )->Show( inputDataEntity, false );
		}

		// Add output to the data list and render it
		// After adding the output, the input will automatically be changed to
		// this one
	/*	Core::DataTreeHelper::PublishOutput( 
			m_Processor->GetOutputDataEntityHolder( 0 ), 
			GetRenderingTree( ),
			m_selectedDataEntityHolder );*/
	
	}
	coreCatchExceptionsLogAndNoThrowMacro( 
		"CardiacInitializationPanelWidget::OnModifiedOutputDataEntity")

}

void TemplatePlugin::SandboxPanelWidget::UpdateHelperWidget()
{
	if ( GetHelperWidget( ) == NULL )
	{
		return;
	}
		GetHelperWidget( )->SetInfo( 
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

Core::BaseProcessor::Pointer TemplatePlugin::SandboxPanelWidget::GetProcessor()
{
	return m_Processor.GetPointer( );
}
