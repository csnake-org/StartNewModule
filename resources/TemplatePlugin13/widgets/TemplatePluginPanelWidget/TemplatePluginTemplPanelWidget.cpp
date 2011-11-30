/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "TemplatePluginTemplPanelWidget.h"

// GuiBridgeLib
#include "gblWxBridgeLib.h"
#include "gblWxButtonEventProxy.h"
// Core
#include "coreDataEntityHelper.h"
#include "coreUserHelperWidget.h"

// Core
#include "coreDataTreeHelper.h"
#include "coreReportExceptionMacros.h"


TemplatePlugin::TemplPanelWidget::TemplPanelWidget(  wxWindow* parent, int id/*= wxID_ANY*/,
													   const wxPoint&  pos /*= wxDefaultPosition*/, 
													   const wxSize&  size /*= wxDefaultSize*/, 
													   long style/* = 0*/ )
: TemplatePluginTemplPanelWidgetUI(parent, id,pos,size,style)
{
	m_Processor = TemplatePlugin::TemplProcessor::New();

	SetName( "Templ Panel Widget" );
}

TemplatePlugin::TemplPanelWidget::~TemplPanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void TemplatePlugin::TemplPanelWidget::OnInit( )
{
	//------------------------------------------------------
	// Observers to data
	m_Processor->GetOutputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&TemplPanelWidget::OnModifiedOutputDataEntity );

	m_Processor->GetInputDataEntityHolder( TemplProcessor::INPUT_0 )->AddObserver( 
		this, 
		&TemplPanelWidget::OnModifiedInputDataEntity );


	UpdateWidget();
}

void TemplatePlugin::TemplPanelWidget::UpdateWidget()
{
	
	UpdateHelperWidget( );

}

void TemplatePlugin::TemplPanelWidget::UpdateData()
{
	// Set parameters to processor. Pending
}

void TemplatePlugin::TemplPanelWidget::OnBtnApply(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		// Update the scale values from widget to processor
		UpdateData();

		m_Processor->Update( );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "TemplPanelWidget::OnBtnApply" );
}


void TemplatePlugin::TemplPanelWidget::OnModifiedOutputDataEntity()
{
	try{

		Core::DataEntity::Pointer inputDataEntity;
		inputDataEntity = m_Processor->GetInputDataEntity( TemplProcessor::INPUT_0 );

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

void TemplatePlugin::TemplPanelWidget::UpdateHelperWidget()
{
	if ( GetHelperWidget( ) == NULL )
	{
		return;
	}
		GetHelperWidget( )->SetInfo( 
			Core::Widgets::HELPER_INFO_LEFT_BUTTON, 
			" info that is useful in order to use the processor" );

}

bool TemplatePlugin::TemplPanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = TemplatePluginTemplPanelWidgetUI::Enable( enable );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void TemplatePlugin::TemplPanelWidget::OnModifiedInputDataEntity()
{
	UpdateWidget();
}

Core::BaseProcessor::Pointer TemplatePlugin::TemplPanelWidget::GetProcessor()
{
	return m_Processor.GetPointer( );
}
