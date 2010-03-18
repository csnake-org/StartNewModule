/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginSubtractPanelWidget.h"

// GuiBridgeLib
#include "gblWxBridgeLib.h"
#include "gblWxButtonEventProxy.h"
// Core
#include "coreDataEntityHelper.h"
#include "coreUserHelperWidget.h"
#include "coreDataEntityListBrowser.h"
#include "coreReportExceptionMacros.h"
// Core
#include "coreAcquireDataEntityInputControl.h"
#include "coreDataTreeHelper.h"

// Event the widget
BEGIN_EVENT_TABLE(SandboxPlugin::SubtractPanelWidget, SandboxPluginSubtractPanelWidgetUI)
	EVT_BUTTON(wxID_BTN_SUBTRACT, SandboxPlugin::SubtractPanelWidget::OnBtnApply)
END_EVENT_TABLE()

SandboxPlugin::SubtractPanelWidget::SubtractPanelWidget( wxWindow* parent, int id )
: SandboxPluginSubtractPanelWidgetUI(parent, id)
{
	// Init input control widget
	m_AcquireInputWidget = new Core::Widgets::AcquireDataEntityInputControl(
		this, 
		wxID_ANY,
		false);
	GetSizer()->Insert(0, m_AcquireInputWidget, 0, wxEXPAND | wxALL, 4);

	// Init input control widget2
	m_AcquireInputWidget2 = new Core::Widgets::AcquireDataEntityInputControl(
		this, 
		wxID_ANY,
		false );
	GetSizer()->Insert(0, m_AcquireInputWidget2, 0, wxEXPAND | wxALL, 4);

	SetLabel( "Subtract images" );
	
}

SandboxPlugin::SubtractPanelWidget::~SubtractPanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void SandboxPlugin::SubtractPanelWidget::Init( 
	SandboxPlugin::SubtractProcessor::Pointer processor,
	Core::RenderingTree::Pointer tree,
	Core::Widgets::DataEntityListBrowser* listBrowser,
	Core::Widgets::UserHelper *helperWidget )
{
	m_Processor = processor;
	m_RenderingTree = tree;
	m_helperWidget = helperWidget;
	m_selectedDataEntityHolder = listBrowser->GetSelectedDataEntityHolder();

	//Input 1 data
	m_AcquireInputWidget->SetDataEntityListBrowser( listBrowser );
	m_AcquireInputWidget->SetAcquiredInputDataHolder( 
		m_Processor->GetInputDataEntityHolder( 0 ),
		Core::DataEntity::ImageTypeId );
	m_AcquireInputWidget->SetHeaderText( m_Processor->GetInputDataName( 0 ) );

	//Input 2 data
	m_AcquireInputWidget2->SetDataEntityListBrowser( listBrowser );
	m_AcquireInputWidget2->SetAcquiredInputDataHolder( 
		m_Processor->GetInputDataEntityHolder( 1 ),
		Core::DataEntity::ImageTypeId );
	m_AcquireInputWidget2->SetHeaderText( m_Processor->GetInputDataName( 1 ) );

	// Observers to data
	m_Processor->GetOutputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&SubtractPanelWidget::OnModifiedOutputDataEntity );

	m_Processor->GetInputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&SubtractPanelWidget::OnModifiedInputDataEntity );

	UpdateWidget();
}

void SandboxPlugin::SubtractPanelWidget::UpdateWidget()
{
	// Check that the working data is initialized
	if( !m_Processor )
	{
		Enable(false);
		return;
	}

	// Disable automatic update of the widget to avoid recursively calls
	Validate();
}

bool SandboxPlugin::SubtractPanelWidget::Validate()
{
	bool okay = true;

	// Validate each text control. Pending
	return okay;
}

void SandboxPlugin::SubtractPanelWidget::OnBtnApply(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		m_Processor->Update( );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "SubtractPanelWidget::OnBtnApply" );
}


void SandboxPlugin::SubtractPanelWidget::OnModifiedOutputDataEntity()
{
	try{

		// Hide inputs
		m_RenderingTree->Show( m_Processor->GetInputDataEntity( 0 ), false );
		m_RenderingTree->Show( m_Processor->GetInputDataEntity( 1 ), false );

		// Add output to the data list and render it
		// After adding the output, the input will automatically be changed to
		// this one
		Core::DataTreeHelper::PublishOutput( 
			m_Processor->GetOutputDataEntityHolder(0), 
			m_RenderingTree,
			m_selectedDataEntityHolder );
	
	}
	coreCatchExceptionsLogAndNoThrowMacro( 
		"CardiacInitializationPanelWidget::OnModifiedOutputDataEntity")

}

void SandboxPlugin::SubtractPanelWidget::UpdateHelperWidget()
{
	std::string strText = "";
	if (m_Processor->GetInputDataEntity( 0 ).IsNull( ) )
	{
		strText = "Please select input data";
	}
	else
	{
		strText = "Please press button Apply";
	}

	m_helperWidget->SetInfo( 
		Core::Widgets::HELPER_INFO_ONLY_TEXT, strText );
}

bool SandboxPlugin::SubtractPanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = SandboxPluginSubtractPanelWidgetUI::Enable( enable );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void SandboxPlugin::SubtractPanelWidget::OnModifiedInputDataEntity()
{
	UpdateHelperWidget();
}

