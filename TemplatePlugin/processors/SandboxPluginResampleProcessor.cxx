/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginResampleProcessor.h"

#include <string>
#include <iostream>

#include "coreReportExceptionMacros.h"
#include "coreDataEntity.h"
#include "coreDataEntityHelper.h"
#include "coreDataEntityHelper.txx"
#include "coreKernel.h"

#include "itkResampleImageFilter.h"

#include "vtkSmartPointer.h"

SandboxPlugin::ResampleProcessor::ResampleProcessor( )
{
	ProcessorWorkingData::SetNumberOfInputs( 2 );
	ProcessorWorkingData::SetInputDataName( INPUT_IMAGE, "Input Image" );
	ProcessorWorkingData::SetInputDataName( INPUT_POINT, "Input Point" );
	ProcessorWorkingData::SetNumberOfOutputs( 1 );

	// Build data entity for selected point
	Core::DataEntity::Pointer dataEntity;
	dataEntity = Core::DataEntityFactory::Build( 
		NULL,
		Core::DataEntityFactory::VtkPointSet,
		"Input Point",
		1 );
	ProcessorWorkingData::GetInputDataEntityHolder( INPUT_POINT )->SetSubject( dataEntity );

	// Set initial point
	Core::vtkPolyDataPtr vtkInputPoint;
	Core::DataEntityHelper::GetProcessingData( 
		GetInputDataEntityHolder( INPUT_POINT ),
		vtkInputPoint );
	vtkSmartPointer<vtkPoints> pointsVtk = vtkSmartPointer<vtkPoints>::New();
	pointsVtk->SetNumberOfPoints( 1 );
	pointsVtk->SetPoint( 0 , 0, 0, 0 );
	vtkInputPoint->SetPoints( pointsVtk );

	// Create default transform
	m_ScaleTransform = ScaleTransformType::New( );
	ScaleTransformType::ScaleType scale;
	scale[ 0 ] = 0.5;
	scale[ 1 ] = 0.5;
	scale[ 2 ] = 0.5;
	m_ScaleTransform->SetScale( scale );
}

SandboxPlugin::ResampleProcessor::~ResampleProcessor()
{
}

void SandboxPlugin::ResampleProcessor::Update()
{
	try
	{
		// Get the first image
		ImageType::Pointer itkInputImage;
		Core::DataEntityHelper::GetProcessingITKData<ImageType>(
			GetInputDataEntityHolder( INPUT_IMAGE ),
			itkInputImage);

		Core::vtkPolyDataPtr vtkInputPoint;
		Core::DataEntityHelper::GetProcessingData( 
			GetInputDataEntityHolder( INPUT_POINT ),
			vtkInputPoint );

		// Set state to processing (dialog box)
		Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
			Core::Runtime::APP_STATE_PROCESSING );

		ScaleTransformType::InputPointType point;
		double vtkPoint[ 3 ];
		vtkInputPoint->GetPoint( 0, vtkPoint );
		point[ 0 ] = vtkPoint[ 0 ];
		point[ 1 ] = vtkPoint[ 1 ];
		point[ 2 ] = vtkPoint[ 2 ];
		m_ScaleTransform->SetCenter( point );

		// Call the function 
		typedef itk::ResampleImageFilter<ImageType,ImageType> ResampleImageFilterType;
		ResampleImageFilterType::Pointer filter = ResampleImageFilterType::New( );
		filter->SetInput( itkInputImage );
		filter->SetTransform( m_ScaleTransform );
		filter->SetOutputParametersFromImage( itkInputImage );
		filter->Update( );

		// Show message
		OnOperationFinished( "ResampleProcessor" );

		// Set the output to the output of this processor
		UpdateOutputImageAsVtk<ImageType>( 0 ,filter->GetOutput(), "ResampleProcessor");	
	}
	catch(...)
	{
		// Throw the exception again to be catched by the Widget and
		// show a message box with the error message
		Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
			Core::Runtime::APP_STATE_IDLE );

		throw;
	}

	Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
		Core::Runtime::APP_STATE_IDLE );

}

SandboxPlugin::ResampleProcessor::ScaleTransformType::Pointer 
SandboxPlugin::ResampleProcessor::GetScaleTransform() const
{
	return m_ScaleTransform;
}
