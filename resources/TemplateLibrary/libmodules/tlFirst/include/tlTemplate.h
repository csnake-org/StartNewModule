/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/
#ifndef TLTEMPLATE_H
#define TLTEMPLATE_H

// Add the include file of your library, to use the TEMPLATELIBRARY_EXPORT macro
#include "TemplateLibraryWin32Header.h"

// baselib
#include "blLightObject.h"

namespace tl
{

/** 
\brief Brief description of this class.
\ingroup TemplateLibrary
*/
class TEMPLATELIBRARY_EXPORT Template : public blLightObject
{

public:

    typedef Template Self;
    typedef blSmartPointer<Self> Pointer;

    //! New macro.
    blNewMacro( Self );

    //! Get width.
    int GetWidth() const;

    //! Set width.
    void SetWidth( int val );

protected:

    //! Constructor: protect from instantiation.
    Template();

    //! Desctructor: protect from instantiation.
    ~Template();

private:

    //! Copy constructor: purposely not implemented.
    Template( const Self& );

    //! Assignement operator: purposely not implemented.
    void operator = ( const Self& );

    //! Width
    int m_width;

}; // class Template

} // namespace tl

#endif //TLTEMPLATE_H
