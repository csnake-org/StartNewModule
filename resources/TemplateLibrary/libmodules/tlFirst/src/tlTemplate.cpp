/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/
#include "tlTemplate.h"

tl::Template::Template()
{
    m_width = 10;
}

tl::Template::~Template()
{
}

int tl::Template::GetWidth() const
{
    return m_width;
}

void tl::Template::SetWidth( int val )
{
    m_width = val;
}
