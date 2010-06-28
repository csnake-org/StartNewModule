import wx

class HelpDialog(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: HelpDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Frame.__init__(self, *args, **kwds)
        
        text = ""
        text += "1. Put the name you want for your module in field Name\n"
        text += "    * for type \"library\" put something like MyNewNameLib\n"
        text += "    * for type \"Gimias Plugin\" put something like MyNewNamePlugin\n"
        text += "    * for type \"Gimias Plugin widget\" put only MyNewFunctionality it will add\n"
        text += "       automatically PanelWidget and Processor\n"
        text += "    * for type \"ThirdParty\" put something likt MyNewThirdParty\n"
        text += "2. Set the root path to your module:\n"
        text += "    * for type \"library\" MySrcFolder/src/cilabModules or MySrcFolder/src/modules\n"
        text += "    * for type \"Gimias Plugin\" MySrcFolder/src/Apps/Plugins or\n"
        text += "       MySrcFolder/src/plugins\n"
        text += "    * for type \"Gimias Plugin widget\" MySrcFolder/src/Apps/Plugins/MyNewNamePlugin\n"
        text += "       or MySrcFolder/src/plugins/MyNewNamePlugin\n"
        text += "    * for type \"ThirdParty\" MySrcFolder/thirdParty or MySrcFolder/src/thirdparties\n"
        text += "3. Select Type \"library\" or \"Gimias Plugin\" or \"Gimias Plugin widget\"\n"
        text += "    or \"ThirdParty\"\n"
        text += "4. (for type \"library\", \"Gimias Plugin\" and \"ThirdParty\"  only) Set Toolkit csn file\n"
        text += "    to your MySrcFolder/src/csnCISTIBToolkit.py or csnMyToolkit.py\n"
        text += "5. (for type \"Gimias Plugin\" only) Set your Gimias csn file to your\n"
        text += "    MySrcFolder/src/Apps/csnGIMIAS.py or MySrcFolder/src/csnGIMIAS.py\n"
        text += "6. Press on StartNewModule\n"

        self.textBasicHelp = wx.TextCtrl(self, -1, text, style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: HelpDialog.__set_properties
        self.SetTitle("Basic Help")
        self.SetSize((600, 350))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: HelpDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.textBasicHelp, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
