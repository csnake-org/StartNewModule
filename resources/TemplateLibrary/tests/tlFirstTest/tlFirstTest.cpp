/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include "tlFirstTest.h"
#include "tlTemplate.h"

void tlFirstTest::TestFirst( )
{
	tl::Template::Pointer tem = tl::Template::New( );

	TS_ASSERT_EQUALS(tem->GetWidth( ),10);
}


