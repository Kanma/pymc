#! /usr/bin/env python

import wx
from ui import MainWindow
from processing.ast import DeclarationsList


class Application(wx.App):

    def __init__(self):
        self.mainWindow = None
        self.declarations = DeclarationsList()

        wx.App.__init__(self, redirect=False)
        

    def OnInit(self):
        self.mainWindow = MainWindow(None, -1, "Python Module Creator (PyMC)")

        screen_rect = wx.Display(wx.Display.GetFromWindow(self.mainWindow)).GetGeometry()
        window_size = self.mainWindow.GetSize()

        window_size.width = max(window_size.width, screen_rect.width - 100)
        window_size.height = max(window_size.height, screen_rect.height - 100)

        self.mainWindow.SetDimensions((screen_rect.width - window_size.width) / 2,
                                      (screen_rect.height - window_size.height) / 2,
                                      window_size.width, window_size.height)
        self.mainWindow.Show(True)

        self.SetTopWindow(self.mainWindow)

        

        return True

    
    def CreateProject(self, event=None):
        pass


    def OpenProject(self, event=None):
        pass


    def Save(self, event=None):
        pass


    def Parse(self, event=None):
        pass


    def Generate(self, event=None):
        pass


if __name__ == '__main__':
    app = Application()
    app.MainLoop()
