/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "TemplatePluginTemplateWidgetPanelWidget.h"

// GuiBridgeLib
#include "gblWxBridgeLib.h"
#include "gblWxButtonEventProxy.h"
// Core
#include "coreDataEntityHelper.h"
#include "coreUserHelperWidget.h"
#include "coreFactoryManager.h"
#include "coreProcessorManager.h"

// Core
#include "coreDataTreeHelper.h"
#include "coreReportExceptionMacros.h"

namespace templatePlugin
{

TemplateWidgetPanelWidget::TemplateWidgetPanelWidget(  wxWindow* parent, int id/*= wxID_ANY*/,
    const wxPoint&  pos /*= wxDefaultPosition*/, 
    const wxSize&  size /*= wxDefaultSize*/, 
    long style/* = 0*/ )
: TemplatePluginTemplateWidgetPanelWidgetUI(parent, id,pos,size,style)
{
	m_Processor = templatePlugin::TemplateWidgetProcessor::New();

	SetName( "Templ Panel Widget" );
}

TemplateWidgetPanelWidget::~TemplateWidgetPanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void TemplateWidgetPanelWidget::OnInit( )
{
	//------------------------------------------------------
	// Observers to data
	m_Processor->GetOutputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&TemplateWidgetPanelWidget::OnModifiedOutputDataEntity );

	m_Processor->GetInputDataEntityHolder( TemplateWidgetProcessor::INPUT_0 )->AddObserver( 
		this, 
		&TemplateWidgetPanelWidget::OnModifiedInputDataEntity );


	UpdateWidget();
}

void TemplateWidgetPanelWidget::UpdateWidget()
{
	UpdateHelperWidget( );
}

void TemplateWidgetPanelWidget::UpdateData()
{
	// Set parameters to processor. Pending
}

void TemplateWidgetPanelWidget::OnBtnApply(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		// Update the scale values from widget to processor
		UpdateData();

        // Set multithreading to false if you want to execute it directly by main GUI thread
        GetProcessor()->SetMultithreading( false );
        Core::Runtime::Kernel::GetProcessorManager()->Execute( GetProcessor() );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "TemplateWidgetPanelWidget::OnBtnApply" );
}


void TemplateWidgetPanelWidget::OnModifiedOutputDataEntity()
{
	try
    {
		Core::DataEntity::Pointer inputDataEntity;
		inputDataEntity = m_Processor->GetInputDataEntity(TemplateWidgetProcessor::INPUT_0 );

		// Hide input if is different from output and output is not empty
		if ( m_Processor->GetOutputDataEntity( 0 ).IsNotNull() && 
			 m_Processor->GetOutputDataEntity( 0 ) != inputDataEntity )
		{
			GetRenderingTree()->Show( inputDataEntity, false );
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
		"TemplateWidgetPanelWidget::OnModifiedOutputDataEntity")
}

void TemplateWidgetPanelWidget::UpdateHelperWidget()
{
	if ( GetHelperWidget( ) == NULL )
	{
		return;
	}
    GetHelperWidget( )->SetInfo( 
        Core::Widgets::HELPER_INFO_LEFT_BUTTON, 
        " info that is useful in order to use the processor" );
}

bool TemplateWidgetPanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = TemplatePluginTemplateWidgetPanelWidgetUI::Enable( enable );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void TemplateWidgetPanelWidget::OnModifiedInputDataEntity()
{
	UpdateWidget();
}

Core::BaseProcessor::Pointer TemplateWidgetPanelWidget::GetProcessor()
{
	return m_Processor.GetPointer( );
}

} //namespace templatePlugin
