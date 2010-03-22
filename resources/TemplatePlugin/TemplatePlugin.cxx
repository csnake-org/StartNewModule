/*
* Copyright (c) 2009,
* Computational Image and Simulation Technologies in Biomedicine (CISTIB),
* Universitat Pompeu Fabra (UPF), Barcelona, Spain. All rights reserved.
* See license.txt file for details.
*/

// For compilers that don't support precompilation, include "wx/wx.h"
#include <wx/wxprec.h>

#ifndef WX_PRECOMP
       #include <wx/wx.h>
#endif

#include "TemplatePlugin.h"

// CoreLib
#include "coreReportExceptionMacros.h"
#include "coreWxMitkGraphicalInterface.h"
#include "corePluginTab.h"

// Declaration of the plugin
coreBeginDefinePluginMacro(TemplatePlugin::TemplatePlugin)
	coreDefinePluginAddProfileMacro("TemplatePlugin")
coreEndDefinePluginMacro()

TemplatePlugin::TemplatePlugin::TemplatePlugin(void) : FrontEndPlugin("TemplatePlugin")
{
	try
	{
		corePluginMacroCreatePluginTab( this );

		m_Processors = ProcessorCollective::New();
		m_Widgets = WidgetCollective::New();
		m_Widgets->Init( m_Processors, this );
	}
	coreCatchExceptionsReportAndNoThrowMacro(TemplatePlugin::TemplatePlugin)
}

TemplatePlugin::TemplatePlugin::~TemplatePlugin(void)
{
}
