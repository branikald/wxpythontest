import wx
import wx.dataview as dv
from random import randint, choice
from collections import namedtuple
import sys
Detail = namedtuple('Detail', 'chto, naim, route')


# объявление ноды как namedtuple не разрешает использование слабых ссылок (UseWeakRefs) для модели дерева
# Node = namedtuple('Node', 'd, num, parent, children')
class Node:
    def __init__(self, det, count, parent, children):
        self.d = det
        self.num = count
        self.parent = parent
        self.children = children


# generate sample data
DB = [Detail(i, "Деталь" + str(randint(1000, 80000)), '0310 ' * 6) for i in range(40000)]  # генерируем БД деталей
root_nodes = [Node(Detail(40000 + i, "Редуктор" + str(i), '1190 ' * 3), randint(1, 40), None, []) for i in range(1000)]

for n in root_nodes:
    for i in range(randint(3, 100)):
        ch = Node(choice(DB), randint(1, 10), n, None)
        if i < 10:
            for j in range(randint(2, 40)):
                cch = Node(choice(DB), randint(1, 10), ch, None)
                if ch.children is None:
                    ch.children = []
                ch.children.append(cch)
        n.children.append(ch)


# Debug print
# for n in root_nodes:
#     print(n.d.naim)
#     for c in n.children:
#         print(f'\t{c.d.naim}\t{c.num}')

class DetailsTreeModel(dv.PyDataViewModel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        super().UseWeakRefs(True)

    def IsContainer(self, item):
        if not item:
            return True
        node = self.ItemToObject(item)
        return node.children is not None

    def GetColumnType(self, col):
        return 'str'

    def GetParent(self, item):
        if not item:
            return dv.NullDataViewItem
        node = self.ItemToObject(item)
        return self.ObjectToItem(node.parent) if node.parent else dv.NullDataViewItem

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for item in self.data:
                children.append(self.ObjectToItem(item))
            return len(self.data)
        node = self.ItemToObject(parent)
        for item in node.children:
            children.append(self.ObjectToItem(item))
        return len(node.children)

    def HasContainerColumns(self, item):
        return True

    def GetColumnCount(self):
        return 3  # Наименование, КУ, КИ, КП, Маршрут, Материал

    def GetValue(self, item, col):
        node = self.ItemToObject(item)
        if col == 0:
            return node.d.naim
        elif col == 1:
            return str(node.num)
        elif col == 2:
            return str(node.d.route)
        return ""

    def SetValue(self, variant, item, col):
        pass

    def GetAttr(self, item, col, attr):
        if self.IsContainer(item):
            attr.Bold = True
            return True
        return False


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.monoFont = wx.Font(wx.FontInfo(10).Family(wx.FONTFAMILY_TELETYPE))

        self.SetSizeHints(minSize=(1024, 600))
        splitterV = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.treeCtl = dv.DataViewCtrl(splitterV, style=dv.DV_VERT_RULES | dv.DV_HORIZ_RULES | dv.DV_MULTIPLE)
        self.treeCtl.SetFont(self.monoFont)
        model = DetailsTreeModel(root_nodes)
        self.treeCtl.AssociateModel(model)
        self.treeCtl.AppendTextColumn('Деталь', 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.treeCtl.AppendTextColumn('Кол-во', 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.treeCtl.AppendTextColumn('Маршрут', 2, width=wx.COL_WIDTH_AUTOSIZE)

        splitterH = wx.SplitterWindow(splitterV, style=wx.SP_LIVE_UPDATE)
        # Текстовые поля для вывода операций и информации о детали
        self.operations = wx.TextCtrl(splitterH, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NOHIDESEL)
        self.operations.SetFont(self.monoFont)
        self.detailInfo = wx.TextCtrl(splitterH, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NOHIDESEL)
        self.detailInfo.SetFont(self.monoFont)

        splitterH.SetSashGravity(0.5)
        splitterH.SplitHorizontally(self.operations, self.detailInfo, -300)
        splitterH.SetMinimumPaneSize(100)

        splitterV.SetSashGravity(0.8)
        splitterV.SplitVertically(self.treeCtl, splitterH, -300)
        splitterV.SetMinimumPaneSize(400)

    def OnSelectItem(self, event):
        wx.Sleep(25)
        pass
    # itemid = event.GetEventObject().GetSelection() # return selected item's index
    # self.textbox.SetValue (event.GetString())


def main():
    app = wx.App()
    frame = MainWindow(None, "Custom tree test")
    frame.Show()
    if sys.platform.startswith('linux'):
        import resource
        print("Memory: {:.1f} mb".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))  # memory usage total, Mb
    app.MainLoop()


if __name__ == '__main__':
    main()
