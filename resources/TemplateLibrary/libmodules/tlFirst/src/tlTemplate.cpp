/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/
#include "tlTemplate.h"

namespace tl
{

Template::Template() : m_width( 10 )
{
}

Template::~Template()
{
}

int Template::GetWidth() const
{
    return m_width;
}

void Template::SetWidth( int val )
{
    m_width = val;
}

} //  namespace tl
