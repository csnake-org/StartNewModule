import wx

class HelpDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: HelpDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.textBasicHelp = wx.TextCtrl(self, -1, "First This, then that...", style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: HelpDialog.__set_properties
        self.SetTitle("Basic Help")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: HelpDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.textBasicHelp, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
