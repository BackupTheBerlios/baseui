# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May  4 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class Database
###########################################################################

class Database ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,260 ), style = wx.TAB_TRAVERSAL )
		
		self.SetMinSize( wx.Size( 200,260 ) )
		
		frame_database = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Datenbank" ), wx.VERTICAL )
		
		sizer_content = wx.FlexGridSizer( 2, 2, 0, 0 )
		sizer_content.AddGrowableCol( 1 )
		sizer_content.SetFlexibleDirection( wx.BOTH )
		sizer_content.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_engine = wx.StaticText( self, wx.ID_ANY, u"Engine", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_engine.Wrap( -1 )
		sizer_content.Add( self.label_engine, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		combobox_engineChoices = []
		self.combobox_engine = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combobox_engineChoices, 0 )
		sizer_content.Add( self.combobox_engine, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_database = wx.StaticText( self, wx.ID_ANY, u"Datenbank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_database.Wrap( -1 )
		sizer_content.Add( self.label_database, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_database = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_content.Add( self.entry_database, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_odbc = wx.StaticText( self, wx.ID_ANY, u"ODBC-Treiber", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_odbc.Wrap( -1 )
		sizer_content.Add( self.label_odbc, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		combobox_odbcChoices = []
		self.combobox_odbc = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combobox_odbcChoices, 0 )
		sizer_content.Add( self.combobox_odbc, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_host = wx.StaticText( self, wx.ID_ANY, u"Host", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_host.Wrap( -1 )
		sizer_content.Add( self.label_host, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_host = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_content.Add( self.entry_host, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_user = wx.StaticText( self, wx.ID_ANY, u"Benutzer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_user.Wrap( -1 )
		sizer_content.Add( self.label_user, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_user = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_content.Add( self.entry_user, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_password = wx.StaticText( self, wx.ID_ANY, u"Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_password.Wrap( -1 )
		sizer_content.Add( self.label_password, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		sizer_content.Add( self.entry_password, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizer_content.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.sizer_button = wx.BoxSizer( wx.VERTICAL )
		
		sizer_content.Add( self.sizer_button, 1, wx.EXPAND, 5 )
		
		frame_database.Add( sizer_content, 1, wx.EXPAND, 5 )
		
		self.SetSizer( frame_database )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class Login
###########################################################################

class Login ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,100 ), style = wx.TAB_TRAVERSAL )
		
		self.SetMinSize( wx.Size( 200,100 ) )
		
		frame_login = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Login" ), wx.VERTICAL )
		
		sizer_content = wx.FlexGridSizer( 2, 2, 0, 0 )
		sizer_content.AddGrowableCol( 1 )
		sizer_content.SetFlexibleDirection( wx.BOTH )
		sizer_content.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_user = wx.StaticText( self, wx.ID_ANY, u"Benutzer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_user.Wrap( -1 )
		sizer_content.Add( self.label_user, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		combobox_userChoices = []
		self.combobox_user = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combobox_userChoices, 0 )
		sizer_content.Add( self.combobox_user, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_password = wx.StaticText( self, wx.ID_ANY, u"Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_password.Wrap( -1 )
		sizer_content.Add( self.label_password, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		sizer_content.Add( self.entry_password, 0, wx.ALL|wx.EXPAND, 5 )
		
		frame_login.Add( sizer_content, 1, wx.EXPAND, 5 )
		
		self.SetSizer( frame_login )
		self.Layout()
	
	def __del__( self ):
		pass
	

