/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginShapeScalePanelWidget.h"

// GuiBridgeLib
#include "gblWxBridgeLib.h"
#include "gblWxButtonEventProxy.h"

// Core
#include "coreVTKPolyDataHolder.h"
#include "coreDataEntityHelper.h"
#include "coreUserHelperWidget.h"
#include "coreRenderingTree.h"
#include "coreDataEntityListBrowser.h"
#include "coreReportExceptionMacros.h"

// STD
#include <limits>

// Core
#include "coreAcquireDataEntityInputControl.h"
#include "coreDataTreeHelper.h"

// Event the widget
BEGIN_EVENT_TABLE(SandboxPlugin::ShapeScalePanelWidget, SandboxPluginShapeScalePanelWidgetUI)
	EVT_BUTTON(wxID_BTN_SCALE, SandboxPlugin::ShapeScalePanelWidget::OnBtnScale)
END_EVENT_TABLE()

SandboxPlugin::ShapeScalePanelWidget::ShapeScalePanelWidget( wxWindow* parent, int id )
: SandboxPluginShapeScalePanelWidgetUI(parent, id)
{
	SetLabel( "SandboxPluginShapeScale" );

	// Init input control widget
	m_AcquireInputWidget = new Core::Widgets::AcquireDataEntityInputControl(
		this, 
		wxID_ANY,
		true );
	GetSizer()->Insert(0, m_AcquireInputWidget, 0, wxEXPAND | wxALL, 4);

	// Each time a text control is modified, this function will be called
	m_changeInWidgetObserver.SetSlotFunction(this, &ShapeScalePanelWidget::UpdateData);
	m_changeInWidgetObserver.Observe(m_textScale);
}

SandboxPlugin::ShapeScalePanelWidget::~ShapeScalePanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void SandboxPlugin::ShapeScalePanelWidget::Init( 
	SandboxPlugin::ShapeScaleProcessor::Pointer processor,
	Core::RenderingTree::Pointer tree,
	Core::Widgets::DataEntityListBrowser* listBrowser,
	Core::Widgets::UserHelper *helperWidget )
{
	m_Processor = processor;
	m_RenderingTree = tree;
	m_helperWidget = helperWidget;

	m_AcquireInputWidget->SetDataEntityListBrowser( listBrowser );
	m_AcquireInputWidget->SetAcquiredInputDataHolder( 
		m_Processor->GetInputDataEntityHolder( 0 ),
		Core::DataEntity::SurfaceMeshTypeId );
	m_AcquireInputWidget->SetHeaderText( m_Processor->GetInputDataName( 0 ) );

	m_Processor->GetParametersHolder()->AddObserver(
		this, &ShapeScalePanelWidget::UpdateWidget);
	m_Processor->GetOutputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&ShapeScalePanelWidget::OnModifiedOutputDataEntity );
	m_Processor->GetInputDataEntityHolder( 0 )->AddObserver( 
		this, 
		&ShapeScalePanelWidget::OnModifiedInputDataEntity );

	UpdateWidget();
}

void SandboxPlugin::ShapeScalePanelWidget::UpdateWidget()
{
	// Check that the working data is initialized
	if( !m_Processor )
	{
		Enable(false);
		return;
	}

	// Disable automatic update of the widget to avoid recursively calls
	m_changeInWidgetObserver.SetEnabled(false);

	float fScale = m_Processor->GetParametersHolder()->GetSubject( );

	// Update each text control with the parameters of the WorkingData
	const int maxNrDecimals = 6;
	gbl::SetNumber(m_textScale, fScale, maxNrDecimals );

	m_changeInWidgetObserver.SetEnabled(true);
	Validate();

	// Update user helper
	UpdateHelperWidget( );
}

bool SandboxPlugin::ShapeScalePanelWidget::Validate()
{
	bool okay = true;

	// Validate each text control. Pending
	return okay;
}

void SandboxPlugin::ShapeScalePanelWidget::UpdateData()
{
	if( !Validate() )
		return;

	float fScale = 0;

	// Update each paramterer of the WorkingData
	fScale = gbl::GetNumber( m_textScale );

	m_Processor->GetParametersHolder()->SetSubject( fScale );
}

void SandboxPlugin::ShapeScalePanelWidget::OnBtnScale(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		m_Processor->Update( );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "ShapeScalePanelWidget::OnBtnScale" );
}

void SandboxPlugin::ShapeScalePanelWidget::OnModifiedOutputDataEntity()
{
	try{
		// Hide input
		m_RenderingTree->Show( m_Processor->GetInputDataEntity( 0 ), false );

		// Add output to the data list and render it
		// After adding the output, the input will automatically be changed to
		// this one
		Core::DataTreeHelper::PublishOutput( 
			m_Processor->GetOutputDataEntityHolder( 0 ), 
			m_RenderingTree );
	}
	coreCatchExceptionsLogAndNoThrowMacro( 
		"CardiacInitializationPanelWidget::OnModifiedOutputDataEntity")

}

void SandboxPlugin::ShapeScalePanelWidget::UpdateHelperWidget()
{
	std::string strText = "";
	if (m_Processor->GetInputDataEntity( 0 ).IsNull( ) )
	{
		strText = "Please select input data";
	}
	else
	{
		strText = "Please press button";
	}

	m_helperWidget->SetInfo( 
		Core::Widgets::HELPER_INFO_ONLY_TEXT, strText );
}

bool SandboxPlugin::ShapeScalePanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = SandboxPluginShapeScalePanelWidgetUI::Enable( enable );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void SandboxPlugin::ShapeScalePanelWidget::OnModifiedInputDataEntity()
{
	UpdateHelperWidget();
}

