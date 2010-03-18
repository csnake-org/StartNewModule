/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "SandboxPluginShapeScaleProcessor.h"

#include <string>

#include "vtkPolyData.h"

#include "coreReportExceptionMacros.h"
#include "coreDataEntity.h"
#include "coreDataEntityHelper.h"
#include "coreDataEntityHelper.txx"
#include "coreKernel.h"
#include "coreVTKPolyDataHolder.h"

#include "blVTKHelperTools.h"

SandboxPlugin::ShapeScaleProcessor::ShapeScaleProcessor( )
{
	m_ParametersHolder = Core::DataHolder<float>::New();
	m_ParametersHolder->SetSubject( 0.5 );

	ProcessorWorkingData::SetNumberOfInputs( 1 );
	ProcessorWorkingData::SetInputDataName( 0, "Surface mesh" );
	ProcessorWorkingData::SetNumberOfOutputs( 1 );
}

SandboxPlugin::ShapeScaleProcessor::~ShapeScaleProcessor()
{
}

void SandboxPlugin::ShapeScaleProcessor::Update()
{
	try
	{
		// Get the mesh 
		Core::vtkPolyDataPtr vtkInputMesh;
		Core::DataEntityHelper::GetProcessingData( 
			GetInputDataEntityHolder( 0 ),
			vtkInputMesh );

		// Set state to processing (dialog box)
		Core::Runtime::Kernel::GetApplicationRuntime( )->SetAppState( 
			Core::Runtime::APP_STATE_PROCESSING );

		// Call the function
		Core::vtkPolyDataPtr vtkOutputMesh = Core::vtkPolyDataPtr::New();
		blVTKHelperTools::ScaleShape( 
			vtkInputMesh, 
			vtkOutputMesh, 
			GetParametersHolder()->GetSubject( ) );

		// Show message
		OnOperationFinished( "ScaleShape" );

		// Set the output to the output of this processor
		UpdateOutput( 0, vtkOutputMesh, "ScaleShape" );
		
	}
	catch( ... )
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

SandboxPlugin::ShapeScaleProcessor::ParametersHolder::Pointer 
SandboxPlugin::ShapeScaleProcessor::GetParametersHolder() const
{
	return m_ParametersHolder;
}

