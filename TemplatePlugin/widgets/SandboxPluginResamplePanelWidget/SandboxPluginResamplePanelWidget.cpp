/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginResamplePanelWidget.h"

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

// Event the widget
BEGIN_EVENT_TABLE(SandboxPlugin::ResamplePanelWidget, SandboxPluginResamplePanelWidgetUI)
	EVT_BUTTON(wxID_BTN_Resample, SandboxPlugin::ResamplePanelWidget::OnBtnApply)
END_EVENT_TABLE()

SandboxPlugin::ResamplePanelWidget::ResamplePanelWidget( wxWindow* parent, int id )
: SandboxPluginResamplePanelWidgetUI(parent, id)
{
	// Init input control widget
	m_AcquireInputWidget = new Core::Widgets::AcquireDataEntityInputControl(
		this, 
		wxID_ANY,
		true);
	GetSizer()->Insert(0, m_AcquireInputWidget, 0, wxEXPAND | wxALL, 4);

	//m_AcquireInputWidgetPoints = new Core::Widgets::AcquireDataEntityInputControl(
	//	this, 
	//	wxID_ANY,
	//	true);
	//GetSizer()->Insert(1, m_AcquireInputWidgetPoints, 0, wxEXPAND | wxALL, 4);

	SetLabel( "Resample an image" );

}

SandboxPlugin::ResamplePanelWidget::~ResamplePanelWidget( )
{
	// We don't need to destroy anything because all the child windows 
	// of this wxWindow are destroyed automatically
}

void SandboxPlugin::ResamplePanelWidget::Init( 
	SandboxPlugin::ResampleProcessor::Pointer processor,
	Core::RenderingTree::Pointer tree,
	Core::Widgets::DataEntityListBrowser* listBrowser,
	Core::Widgets::UserHelper *helperWidget )
{
	//------------------------------------------------------
	m_Processor = processor;
	m_RenderingTree = tree;
	m_helperWidget = helperWidget;
	m_selectedDataEntityHolder = listBrowser->GetSelectedDataEntityHolder();

	//------------------------------------------------------
	//Input 1 data
	m_AcquireInputWidget->SetDataEntityListBrowser( listBrowser );
	m_AcquireInputWidget->SetAcquiredInputDataHolder( 
		m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_IMAGE ),
		Core::DataEntity::ImageTypeId );
	m_AcquireInputWidget->SetHeaderText( 
		m_Processor->GetInputDataName( ResampleProcessor::INPUT_IMAGE ) );


	//m_AcquireInputWidgetPoints->SetCurrentSelectedDataHolder( 
	//	m_selectedDataEntityHolder,
	//	Core::Runtime::Kernel::GetDataContainer()->GetDataEntityList( ) );
	//m_AcquireInputWidgetPoints->SetAcquiredInputDataHolder( 
	//	m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT ),
	//	Core::DataEntity::PointSetTypeId );
	//m_AcquireInputWidgetPoints->SetHeaderText( 
	//	m_Processor->GetInputDataName( ResampleProcessor::INPUT_POINT ) );


	//------------------------------------------------------
	// Observers to data
	m_Processor->GetOutputDataEntityHolder( ResampleProcessor::INPUT_IMAGE )->AddObserver( 
		this, 
		&ResamplePanelWidget::OnModifiedOutputDataEntity );

	m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_IMAGE )->AddObserver( 
		this, 
		&ResamplePanelWidget::OnModifiedInputDataEntity );

	m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT )->AddObserver( 
		this, 
		&ResamplePanelWidget::OnModifiedInputPoint);

	//------------------------------------------------------
	// Interactor
	m_PointInteractor = Core::PointInteractorPointSelect::New( 
		tree,
		m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT ),
		m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_IMAGE ) );

	UpdateWidget();
}

void SandboxPlugin::ResamplePanelWidget::UpdateWidget()
{
	SandboxPlugin::ResampleProcessor::ScaleTransformType::ScaleType scale;
	scale  = m_Processor->GetScaleTransform( )->GetScale( );

	// Update each text control with the parameters of the WorkingData
	m_SpinCtrlX->SetValue( scale[ 0 ] * 100 );
	m_SpinCtrlY->SetValue( scale[ 1 ] * 100 );
	m_SpinCtrlZ->SetValue( scale[ 2 ] * 100 );

	// Enable Apply button
	bool bInputPointsSelected = false;
	try{
		Core::vtkPolyDataPtr vtkInputPoint;
		Core::DataEntityHelper::GetProcessingData( 
			m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT ),
			vtkInputPoint );
		bInputPointsSelected = vtkInputPoint->GetNumberOfPoints() != 0;
	}catch(...)
	{

	}

	m_btnResample->Enable( bInputPointsSelected );

	UpdateHelperWidget( );

	Validate();
}

void SandboxPlugin::ResamplePanelWidget::UpdateData()
{
	if( !Validate() )
		return;

	SandboxPlugin::ResampleProcessor::ScaleTransformType::ScaleType scale;

	// Update each paramterer of the WorkingData
	scale[ 0 ] = double( m_SpinCtrlX->GetValue( ) ) / 100;
	scale[ 1 ] = double( m_SpinCtrlY->GetValue( ) ) / 100;
	scale[ 2 ] = double( m_SpinCtrlZ->GetValue( ) ) / 100;
	m_Processor->GetScaleTransform( )->SetScale( scale );
}

bool SandboxPlugin::ResamplePanelWidget::Validate()
{
	bool okay = true;

	// Validate each text control. Pending
	return okay;
}


void SandboxPlugin::ResamplePanelWidget::OnBtnApply(wxCommandEvent& event)
{
	// Catch the exception from the processor and show the message box
	try
	{
		// Update the scale values from widget to processor
		UpdateData();

		m_Processor->Update( );
	}
	coreCatchExceptionsReportAndNoThrowMacro( "ResamplePanelWidget::OnBtnApply" );
}


void SandboxPlugin::ResamplePanelWidget::OnModifiedOutputDataEntity()
{
	try{

		Core::DataEntity::Pointer inputDataEntity;
		inputDataEntity = m_Processor->GetInputDataEntity( ResampleProcessor::INPUT_IMAGE );

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

void SandboxPlugin::ResamplePanelWidget::UpdateHelperWidget()
{
	bool bInputPointsSelected = false;
	try{
		Core::vtkPolyDataPtr vtkInputPoint;
		Core::DataEntityHelper::GetProcessingData( 
			m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT ),
			vtkInputPoint );
		bInputPointsSelected = vtkInputPoint->GetNumberOfPoints() != 0;
	}catch( ... )
	{

	}

	if (m_Processor->GetInputDataEntity( ResampleProcessor::INPUT_IMAGE ).IsNull( ) )
	{
		m_helperWidget->SetInfo( 
			Core::Widgets::HELPER_INFO_ONLY_TEXT, 
			"Please select input data" );
	}
	else if ( !bInputPointsSelected )
	{
		m_helperWidget->SetInfo( 
			Core::Widgets::HELPER_INFO_LEFT_BUTTON, 
			" + SHIFT to set the origin" );
	}
	else
	{
		m_helperWidget->SetInfo( 
			Core::Widgets::HELPER_INFO_ONLY_TEXT, 
			"Please press Apply button" );
	}

}

bool SandboxPlugin::ResamplePanelWidget::Enable( bool enable /*= true */ )
{
	bool bReturn = SandboxPluginResamplePanelWidgetUI::Enable( enable );

	UpdateInteractor( );

	// If this panel widget is selected -> Update the widget
	if ( enable )
	{
		UpdateWidget();
	}

	return bReturn;
}

void SandboxPlugin::ResamplePanelWidget::OnModifiedInputDataEntity()
{
	// If the interactor was connected to another image, disconnect it
	m_PointInteractor->DisconnectFromDataTreeNode( );

	// Clear selected point
	Core::vtkPolyDataPtr vtkInputPoint;
	Core::DataEntityHelper::GetProcessingData( 
		m_Processor->GetInputDataEntityHolder( ResampleProcessor::INPUT_POINT ),
		vtkInputPoint );
	vtkInputPoint->GetPoints( )->SetNumberOfPoints( 0 );

	UpdateInteractor( );

	UpdateWidget();
}

void SandboxPlugin::ResamplePanelWidget::OnModifiedInputPoint()
{
	UpdateWidget();
}

void SandboxPlugin::ResamplePanelWidget::UpdateInteractor( )
{
	try
	{
		bool enable = 
			m_Processor->GetInputDataEntity( ResampleProcessor::INPUT_IMAGE ).IsNotNull( )
			&& IsEnabled();

		if ( enable )
		{
			// We need to have the image in the rendering tree before
			// connecting the interactor
			m_RenderingTree->Add( 
				m_Processor->GetInputDataEntity( ResampleProcessor::INPUT_IMAGE ) );

			// Connect to the new image
			m_PointInteractor->ConnectToDataTreeNode( );
		}
		else
		{
			m_PointInteractor->DisconnectFromDataTreeNode( );
		}
	}
	coreCatchExceptionsReportAndNoThrowMacro( "ResamplePanelWidget::UpdateInteractor" );
}

