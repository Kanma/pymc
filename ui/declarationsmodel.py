import wx
import wx.dataview as dv
import processing.ast as ast


class DeclarationsModel(dv.PyDataViewModel):

    def __init__(self, declarations):
        super(DeclarationsModel, self).__init__()
        self.declarations = declarations
    
    def GetChildren(self, item, children):
        if not item:
            for declaration in self.declarations:
                children.append(self.ObjectToItem(declaration))
            return self.declarations.size()

        declaration = self.ItemToObject(item)
        if isinstance(declaration, ast.Declaration):
            for child in declaration.children:
                children.append(self.ObjectToItem(child))
            return declaration.children.size()

        return 0

    def GetColumnCount(self):
        return 7

    def GetColumnType(self, col):
        if col in [ 0, 4, 5, 6 ]:
            return "bool"

        return "string"

    def GetParent(self, item):
        if not item:
            return dv.NullDataViewItem

        declaration = self.ItemToObject(item)        
        if isinstance(declaration, ast.Declaration):
            if declaration.parent is not None:
                return self.ObjectToItem(declaration.parent)

        return dv.NullDataViewItem

    def GetValue(self, item, col):
        declaration = self.ItemToObject(item)        
        if isinstance(declaration, ast.Declaration):
            if col == 0:
                return declaration.isExported()
            elif col == 1:
                return declaration.type_name
            elif col == 2:
                return declaration.toString()
            elif col == 3:
                return ast.ACCESS.toString(declaration.accessibility)
            elif col == 4:
                return (declaration.virtuality != ast.VIRTUALITY.NOT_VIRTUAL)
            elif col == 5:
                return declaration.static
            elif col == 6:
                return declaration.const

        return ""
        
    def IsContainer(self, item):
        declaration = self.ItemToObject(item)        
        if isinstance(declaration, ast.Declaration):
            return (declaration.children.size() > 0)
        
        return False

    def SetValue(self, value, item, col):
        decl = self.ItemToObject(item)

        if col == 0:
            if decl.isIgnorable():
                decl.export(value)

                if value:
                    parent = decl.parent
                    while (parent is not None) and not(parent.exported):
                        parent.export(True)
                        self.ItemChanged(self.ObjectToItem(parent))
                        parent = parent.parent
