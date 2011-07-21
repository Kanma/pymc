import wx
import wx.dataview as dv
from declarationsmodel import DeclarationsModel
# from ParametersDialog import *


class DeclarationsTree(dv.DataViewCtrl):

    def __init__(self, parent, id, declarations):
        dv.DataViewCtrl.__init__(self, parent, id, style=dv.DV_SINGLE | dv.DV_HORIZ_RULES | dv.DV_VERT_RULES)

        # Associate some events with methods of this class
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnItemMenu)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.model = DeclarationsModel(declarations)

        self.AssociateModel(self.model)
        self.AppendToggleColumn("X", 0, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.AppendTextColumn("Kind", 1, width=100, align=wx.ALIGN_CENTER)
        self.SetExpanderColumn(self.AppendTextColumn("Name", 2, width=500))
        self.AppendTextColumn("Accessibility", 3, width=100, align=wx.ALIGN_CENTER)
        self.AppendToggleColumn("Virtual", 4, align=wx.ALIGN_CENTER, width=60)
        self.AppendToggleColumn("Static", 5, align=wx.ALIGN_CENTER, width=56)
        self.AppendToggleColumn("Const", 6, align=wx.ALIGN_CENTER, width=56)


    def OnItemMenu(self, event):
        self._displayParameters(event.GetItem())


    def OnKeyDown(self, event):
        selection = self.GetSelection()
        if event.GetKeyCode() == wx.WXK_RETURN:
            self._displayParameters(selection)
        elif event.GetKeyCode() == wx.WXK_SPACE:
            self.model.SetValue(not(self.model.GetValue(selection, 0)), selection, 0)
            self.model.ItemChanged(selection)
        else:
            event.Skip()

    def _displayParameters(self, item):
        pass
        # dlg = ParametersDialog(self.GetParent(), -1, "Parameters", self.GetItemData(item).GetData())
        # dlg.ShowModal()
