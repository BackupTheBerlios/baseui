# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May  4 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class Error
###########################################################################

class Error ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 456,175 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer4 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap_icon = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_bitmap_icon, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		fgSizer1.Add( bSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticText_text = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText_text.Wrap( -1 )
		self.m_staticText_text.SetMinSize( wx.Size( 400,100 ) )
		
		fgSizer1.Add( self.m_staticText_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		fgSizer4.Add( fgSizer1, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.togglebutton_detail = wx.ToggleButton( self, wx.ID_ANY, u"Details", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.togglebutton_detail, 0, wx.ALL, 5 )
		
		self.button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_ok, 0, wx.ALL, 5 )
		
		fgSizer4.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		self.staticline_bottom = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.staticline_bottom.Hide()
		
		fgSizer4.Add( self.staticline_bottom, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.entry_traceback = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		self.entry_traceback.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 73, 90, 90, False, "Courier New" ) )
		self.entry_traceback.Hide()
		self.entry_traceback.SetMinSize( wx.Size( 400,150 ) )
		
		fgSizer4.Add( self.entry_traceback, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.togglebutton_detail.Bind( wx.EVT_TOGGLEBUTTON, self.on_button_detail_toggled )
		self.button_ok.Bind( wx.EVT_BUTTON, self.on_button_ok_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_button_detail_toggled( self, event ):
		event.Skip()
	
	def on_button_ok_clicked( self, event ):
		event.Skip()
	

