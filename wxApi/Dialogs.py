# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Dialogs module
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import traceback
import wx
import res.Dialogs
import Panels
from res import IconSet32


class Help(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)



class Error(res.Dialogs.Error):
    def __init__(self, parent):
        res.Dialogs.Error.__init__(self, parent)
        
        self.m_bitmap_icon.SetBitmap(IconSet32.geterror_32Bitmap())
        
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked)
        self.togglebutton_detail.Bind(wx.EVT_TOGGLEBUTTON, self.on_togglebutton_detail_toggled)
        
        
    def show(self, title='Fehler', instance=None, message='Error'):
        self.togglebutton_detail.SetValue(False)
        if instance <> None:
            detail = traceback.format_exc()
            self.entry_traceback.SetValue(detail)
        
        self.m_staticText_text.SetLabel(message + '\n\n' + str(instance))
        self.SetTitle(title)
        
        self.SetInitialSize()
        self.Centre()
        self.ShowModal()
        
        
    def on_togglebutton_detail_toggled(self, event):
        is_down = event.IsChecked() 
        if is_down:
            self.entry_traceback.Show()
            self.staticline_bottom.Show()
        else:
            self.entry_traceback.Hide()
            self.staticline_bottom.Hide()
        self.SetInitialSize()
        
        
    def on_button_ok_clicked(self, event):
        self.entry_traceback.Hide()
        self.Hide()
        
        
        
class FormTablePreferences(wx.Dialog):
    ID_IMPORT = 201
    ID_EXPORT = 202
    
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size=(640, 480))
    
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        sizer_main = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 0 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.m_panel2 = Panels.TableConfig(self.notebook) #wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #self.notebook.AddPage( self.m_panel2, u"Allgemein", True )
        #self.m_panel3 = Panels.TableImport(self.notebook) #wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #self.notebook.AddPage( self.m_panel3, u"Import", False )
        self.panel_export = Panels.TableExport(self.notebook) #wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.panel_export, u"Export", False )
        
        sizer_main.Add( self.notebook, 1, wx.ALL|wx.EXPAND, 5 )
        
        sizer_bottom = wx.FlexGridSizer( 1, 3, 0, 0 )
        sizer_bottom.AddGrowableCol( 0 )
        sizer_bottom.SetFlexibleDirection( wx.BOTH )
        sizer_bottom.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        sizer_bottom.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_bottom.Add( self.button_ok, 0, wx.ALL, 5 )
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked)

        sizer_main.Add( sizer_bottom, 1, wx.EXPAND, 5 )

        self.SetSizer( sizer_main )
        self.Layout()

        self.Centre( wx.BOTH )
        
        
    def on_button_ok_clicked(self, event=None):
        self.Destroy()



