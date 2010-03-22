/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

#ifndef _tlTemplate_h
#define _tlTemplate_h

// Add the include file of your library, to use the TEMPLATELIBRARY_EXPORT macro
#include "TemplateLibraryWin32Header.h"

// baselib
#include "blLightObject.h"

namespace tl{

/** 
\brief Brief description of this class

\ingroup TemplateLibrary
\author Your name
\date 11 April 2008
*/
class TEMPLATELIBRARY_EXPORT Template : public blLightObject{

public:
	typedef Template Self;
	typedef blSmartPointer<Self> Pointer;

public:
	//! Constructor
	blNewMacro( Self );

	//!
	int GetWidth() const;

	//!
	void SetWidth(int val);

protected:
	//!
	Template( );

	//!
	~Template( );

private:
	//! Purposely not implemented
	Template( const Self& );

	//! Purposely not implemented
	void operator = ( const Self& );

private:
	//! Width
	int m_lWidth;

};

}

#endif //_tlTemplate_h
