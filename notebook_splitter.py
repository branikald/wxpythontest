import wx


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.SetSizeHints(minSize=(600, 400))
        tabs = wx.Notebook(self)
        splitter = wx.SplitterWindow(tabs, style=wx.SP_LIVE_UPDATE)
        listbox = wx.ListBox(splitter, choices=["Item1", "Item2", "Item3", "ItemLast"])
        self.textbox = wx.TextCtrl(splitter, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NOHIDESEL)
        listbox.Bind(wx.EVT_LISTBOX, self.OnSelectItem)
        splitter.SplitVertically(listbox, self.textbox)
        splitter.SetMinimumPaneSize(150)

        tabs.InsertPage(0, splitter, "Страница1", select=False)

        textbox2 = wx.TextCtrl(tabs, style=wx.TE_MULTILINE)
        # ~ textbox2.Hint="Enter your name..." # buggy on gtk
        # ~ f = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT)
        # ~ f.SetFamily(wx.FONTFAMILY_TELETYPE)
        f = wx.Font(wx.FontInfo(10).Family(wx.FONTFAMILY_TELETYPE).Bold())
        textbox2.SetFont(f)

        textbox2.Value = "Text example.\n123456\nРусский текст"
        tabs.InsertPage(1, textbox2, "Страница2", select=True)

    def OnSelectItem(self, event):
        itemid = event.GetEventObject().GetSelection()  # return selected item's index
        self.textbox.SetValue(event.GetString())


def main():
    app = wx.App()
    frame = MainWindow(None, "wxPython notebook/splitter test")
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
