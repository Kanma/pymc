import wx
import wx.dataview as dv
from declarationstree import DeclarationsTree


class MainWindow(wx.Frame):

    def __init__(self, parent, id, title, size=wx.Size(800, 600)):
        wx.Frame.__init__(self, parent, id, title, size=size)

        toolBar = self.CreateToolBar(wx.NO_BORDER | wx.TB_HORIZONTAL | wx.TB_TEXT)
        toolBar.AddLabelTool(1, 'New project', wx.Bitmap('resources/create.png', wx.BITMAP_TYPE_PNG))
        toolBar.AddLabelTool(2, 'Open project', wx.Bitmap('resources/open.png', wx.BITMAP_TYPE_PNG))
        toolBar.AddLabelTool(3, 'Save', wx.Bitmap('resources/save.png', wx.BITMAP_TYPE_PNG))
        toolBar.AddSeparator()
        toolBar.AddLabelTool(4, 'Parse', wx.Bitmap('resources/parse.png', wx.BITMAP_TYPE_PNG))
        toolBar.AddLabelTool(5, 'Generate', wx.Bitmap('resources/generate.png', wx.BITMAP_TYPE_PNG))
        toolBar.Realize()

        toolBar.EnableTool(3, False)
        toolBar.EnableTool(4, False)
        toolBar.EnableTool(5, False)

        self.Bind(wx.EVT_TOOL, wx.GetApp().CreateProject, id=1)
        self.Bind(wx.EVT_TOOL, wx.GetApp().OpenProject, id=2)
        self.Bind(wx.EVT_TOOL, wx.GetApp().Save, id=3)
        self.Bind(wx.EVT_TOOL, wx.GetApp().Parse, id=4)
        self.Bind(wx.EVT_TOOL, wx.GetApp().Generate, id=5)
        
        self.tree = DeclarationsTree(self, -1, wx.GetApp().declarations)
