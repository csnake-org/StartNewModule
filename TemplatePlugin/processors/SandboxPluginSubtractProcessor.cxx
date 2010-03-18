/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginSubtractProcessor.h"

#include <string>
#include <iostream>

#include "coreReportExceptionMacros.h"
#include "coreDataEntity.h"
#include "coreDataEntityHelper.h"
#include "coreDataEntityHelper.txx"
#include "coreKernel.h"

#include "itkSubtractImageFilter.h"

SandboxPlugin::SubtractProcessor::SubtractProcessor( )
{
	ProcessorWorkingData::SetNumberOfInputs( 2 );
	ProcessorWorkingData::SetInputDataName( 0, "Input Image" );
	ProcessorWorkingData::SetInputDataName( 1, "Input Image" );
	ProcessorWorkingData::SetNumberOfOutputs( 1 );
}

SandboxPlugin::SubtractProcessor::~SubtractProcessor()
{
}

void SandboxPlugin::SubtractProcessor::Update()
{
	try
	{
		// Get the first image
		ImageType::Pointer itkInputImage;
		Core::DataEntityHelper::GetProcessingITKData<ImageType>(
			GetInputDataEntityHolder(0),
			itkInputImage);
		
		// Get the second image
		ImageType::Pointer itkInputImage2;
		Core::DataEntityHelper::GetProcessingITKData<ImageType>( 
			GetInputDataEntityHolder( 1 ),
			itkInputImage2 );

		// Set state to processing (dialog box)
		Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
			Core::Runtime::APP_STATE_PROCESSING );

		// Call the function 
		typedef itk::SubtractImageFilter<ImageType> SubtractType;
		SubtractType::Pointer filter = SubtractType::New();
		filter->SetInput1( itkInputImage );
		filter->SetInput2( itkInputImage2 );
		filter->Update();

		ImageType::Pointer itkOutputImage = filter->GetOutput();

		UpdateOutputImageAsVtk<ImageType>( 0 , filter->GetOutput(), "SubtractProcessor");	

		OnOperationFinished( "SubtractProcessor" );
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
