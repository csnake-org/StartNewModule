/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "TemplatePluginSandboxProcessor.h"

#include <string>
#include <iostream>

#include "coreReportExceptionMacros.h"
#include "coreDataEntity.h"
#include "coreDataEntityHelper.h"
#include "coreDataEntityHelper.txx"
#include "coreKernel.h"

#include "vtkSmartPointer.h"

TemplatePlugin::SandboxProcessor::SandboxProcessor( )
{
	ProcessorWorkingData::SetNumberOfInputs( INPUTS_NUMBER );
	GetInputPort(INPUT_0)->SetName(  "Input Image" );
	GetInputPort(INPUT_0)->SetDataEntityType( Core::ImageTypeId);
	GetInputPort(INPUT_1)->SetName(  "Input Surface" );
	GetInputPort(INPUT_1)->SetDataEntityType( Core::SurfaceMeshTypeId);
	ProcessorWorkingData::SetNumberOfOutputs( OUTPUTS_NUMBER );
	
}

TemplatePlugin::SandboxProcessor::~SandboxProcessor()
{
}

void TemplatePlugin::SandboxProcessor::Update()
{
	try
	{
		// Get the first image
		ImageType::Pointer itkInputImage;
		Core::DataEntityHelper::GetProcessingITKData<ImageType>(
			GetInputDataEntityHolder( INPUT_0 ),
			itkInputImage);

		Core::vtkPolyDataPtr vtkInput;
		Core::DataEntityHelper::GetProcessingData( 
			GetInputDataEntityHolder( INPUT_1),
			vtkInput );

		// Set state to processing (dialog box)
		Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
			Core::Runtime::APP_STATE_PROCESSING );

		// here goes the filter or the functions that determine the processor
		// the output should go in the update functions
		
		// Show message
		OnOperationFinished( "SandboxProcessor" );

		// Set the output to the output of this processor
		UpdateOutputImageAsVtk<ImageType>( 0 ,itkInputImage, "SandboxProcessorImage");	
		UpdateOutput(1, vtkInput, "SandboxProcessorSurface");
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
