import wx


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.SetSizeHints(minSize=(800, 500))
        panel = wx.Panel(self)  # создаем панель верхнего уровня

        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label="Путь к файлу:")
        tc = wx.TextCtrl(panel)  # текстовое поле, в которое вводится путь к файлу
        # создаем горизонтальный сайзер с 2мя только что созданными элементами: StaticText и TextCtrl
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)  # flag=wx.RIGHT указывает, что border (отступ) будет только справа
        # flag можно дополнить (|) параметрами wx.EXPAND, wx.SHAPED, wx.FIXED_MINSIZE, wx.ALIGN_XXXX
        # border=8 указвает толщину отступа в пикселях
        hbox1.Add(tc,
                  proportion=1)  # proportion заставляет текстовое поле изменять размер вместе с изменением окна-родителя

        # [vbox строка 1] добавляем в top-level сайзер vbox сформированный hbox1
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # [vbox строка 2] добавляем подзаголовок окна и помещяем его в vbox
        st2 = wx.StaticText(panel, label="Содержимое файла")
        vbox.Add(st2, flag=wx.EXPAND | wx.ALL, border=10)

        # [vbox строка 3] многострочное текстовое поле. растягиваемое и с отступами по 10 пикселей
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(tc2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)

        btn_ok = wx.Button(panel, label='Да')  # , size=(70,30))
        btn_cancel = wx.Button(panel, label='Отмена')  # , size=(70,30))
        # горизонтальный сайзер с 2мя кнопками
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(btn_ok, flag=wx.LEFT, border=10)
        hbox2.Add(btn_cancel, flag=wx.LEFT, border=10)

        # [vbox строка 4] горизонтальный сайзер с 2мя кнопками. hbox2 (с кнопками) выравнять по правому краю
        vbox.Add(hbox2, flag=wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, border=10)
        panel.SetSizer(vbox)


def main():
    app = wx.App()
    frame = MainWindow(None, "KMZ tool")
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
