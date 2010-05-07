/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#include <iostream>
#include "tlTemplate.h"

/**
\brief Your first application
\ingroup TemplateLibrary
*/
void main( int argc, char* argv[] )
{
    tl::Template::Pointer tem = tl::Template::New( );
    std::cout << "Width: " << tem->GetWidth( ) << std::endl;
}
