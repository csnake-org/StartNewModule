/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/
#ifndef TLFIRSTTEST_H
#define TLFIRSTTEST_H

#include <cxxtest/TestSuite.h>

/**
\brief Your first test.
*/
class tlFirstTest : public CxxTest::TestSuite
{
public:

    /** \test Test the tl::Template::GetWidth() method. */
    void TestFirst();

}; // class tlFirstTest

#endif //  TLFIRSTTEST_H
