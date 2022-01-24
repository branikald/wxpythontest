import wx


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.Show()


def main():
    app = wx.App()
    frame = MainWindow(None, "wxPython basic")
    app.MainLoop()


if __name__ == '__main__':
    main()
