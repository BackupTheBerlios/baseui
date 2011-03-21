# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
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
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 340,108 ), style = wx.TAB_TRAVERSAL )
		
		self.SetMinSize( wx.Size( 200,-1 ) )
		
		frame_database = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Datenbank" ), wx.VERTICAL )
		
		sizer_content = wx.FlexGridSizer( 5, 2, 0, 0 )
		sizer_content.AddGrowableCol( 1 )
		sizer_content.SetFlexibleDirection( wx.BOTH )
		sizer_content.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_engine = wx.StaticText( self, wx.ID_ANY, u"Engine", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_engine.Wrap( -1 )
		sizer_content.Add( self.label_engine, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		combobox_engineChoices = []
		self.combobox_engine = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combobox_engineChoices, 0 )
		sizer_content.Add( self.combobox_engine, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_odbc = wx.StaticText( self, wx.ID_ANY, u"ODBC-Treiber", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_odbc.Wrap( -1 )
		self.label_odbc.Hide()
		
		sizer_content.Add( self.label_odbc, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		combobox_odbcChoices = []
		self.combobox_odbc = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combobox_odbcChoices, 0 )
		self.combobox_odbc.Hide()
		
		sizer_content.Add( self.combobox_odbc, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_database = wx.StaticText( self, wx.ID_ANY, u"Datenbank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_database.Wrap( -1 )
		self.label_database.Hide()
		
		sizer_content.Add( self.label_database, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_database = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.entry_database.Hide()
		
		sizer_content.Add( self.entry_database, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_host = wx.StaticText( self, wx.ID_ANY, u"Host", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_host.Wrap( -1 )
		self.label_host.Hide()
		
		sizer_content.Add( self.label_host, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_host = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.entry_host.Hide()
		
		sizer_content.Add( self.entry_host, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_user = wx.StaticText( self, wx.ID_ANY, u"Benutzer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_user.Wrap( -1 )
		self.label_user.Hide()
		
		sizer_content.Add( self.label_user, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_user = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.entry_user.Hide()
		
		sizer_content.Add( self.entry_user, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_password = wx.StaticText( self, wx.ID_ANY, u"Passwort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_password.Wrap( -1 )
		self.label_password.Hide()
		
		sizer_content.Add( self.label_password, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		self.entry_password.Hide()
		
		sizer_content.Add( self.entry_password, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_path = wx.StaticText( self, wx.ID_ANY, u"Dateipfad", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_path.Wrap( -1 )
		self.label_path.Hide()
		
		sizer_content.Add( self.label_path, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.filepicker_path = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.filepicker_path.Hide()
		
		sizer_content.Add( self.filepicker_path, 0, wx.ALL|wx.EXPAND, 5 )
		
		
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
	

###########################################################################
## Class Webserver
###########################################################################

class Webserver ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		frame_webserver = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Webserver" ), wx.VERTICAL )
		
		sizer_content = wx.FlexGridSizer( 5, 2, 0, 0 )
		sizer_content.AddGrowableCol( 1 )
		sizer_content.SetFlexibleDirection( wx.BOTH )
		sizer_content.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_host = wx.StaticText( self, wx.ID_ANY, u"Host", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_host.Wrap( -1 )
		sizer_content.Add( self.label_host, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_host = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_content.Add( self.entry_host, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.label_port = wx.StaticText( self, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_port.Wrap( -1 )
		sizer_content.Add( self.label_port, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entry_port = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		sizer_content.Add( self.entry_port, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizer_content.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.sizer_button = wx.BoxSizer( wx.VERTICAL )
		
		sizer_content.Add( self.sizer_button, 1, wx.EXPAND, 5 )
		
		frame_webserver.Add( sizer_content, 1, wx.EXPAND, 5 )
		
		self.SetSizer( frame_webserver )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class TableImport
###########################################################################

class TableImport ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 647,394 ), style = wx.TAB_TRAVERSAL )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Import-Tabelle" ), wx.VERTICAL )
		
		fgSizer8 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer8.AddGrowableCol( 0 )
		fgSizer8.AddGrowableRow( 1 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer6 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Quelldatei", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer6.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.filepicker_source = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		fgSizer6.Add( self.filepicker_source, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer8.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		self.tree_source = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TR_DEFAULT_STYLE )
		fgSizer8.Add( self.tree_source, 0, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer4.Add( fgSizer8, 1, wx.EXPAND, 5 )
		
		fgSizer4.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Zieltabelle" ), wx.VERTICAL )
		
		fgSizer81 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer81.AddGrowableCol( 0 )
		fgSizer81.AddGrowableRow( 1 )
		fgSizer81.SetFlexibleDirection( wx.BOTH )
		fgSizer81.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer61 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer61.AddGrowableCol( 1 )
		fgSizer61.SetFlexibleDirection( wx.BOTH )
		fgSizer61.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText121 = wx.StaticText( self, wx.ID_ANY, u"Tabelle", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )
		fgSizer61.Add( self.m_staticText121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		combobox_targetChoices = []
		self.combobox_target = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.Size( -1,22 ), combobox_targetChoices, 0 )
		fgSizer61.Add( self.combobox_target, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer81.Add( fgSizer61, 1, wx.EXPAND, 5 )
		
		self.tree_target = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TR_DEFAULT_STYLE )
		fgSizer81.Add( self.tree_target, 0, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer5.Add( fgSizer81, 1, wx.EXPAND, 5 )
		
		fgSizer4.Add( sbSizer5, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer4 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class TableExport
###########################################################################

class TableExport ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 647,394 ), style = wx.TAB_TRAVERSAL )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Export-Tabelle" ), wx.VERTICAL )
		
		fgSizer81 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer81.AddGrowableCol( 0 )
		fgSizer81.AddGrowableRow( 1 )
		fgSizer81.SetFlexibleDirection( wx.BOTH )
		fgSizer81.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer61 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer61.AddGrowableCol( 1 )
		fgSizer61.SetFlexibleDirection( wx.BOTH )
		fgSizer61.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText121 = wx.StaticText( self, wx.ID_ANY, u"Zieldatei", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )
		fgSizer61.Add( self.m_staticText121, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.filepicker_export = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
		fgSizer61.Add( self.filepicker_export, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer61.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.button_export = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer61.Add( self.button_export, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		fgSizer81.Add( fgSizer61, 1, wx.EXPAND, 5 )
		
		sbSizer5.Add( fgSizer81, 1, wx.EXPAND, 5 )
		
		fgSizer4.Add( sbSizer5, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer4 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class TableConfig
###########################################################################

class TableConfig ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 647,394 ), style = wx.TAB_TRAVERSAL )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Spaltenlayout" ), wx.VERTICAL )
		
		fgSizer8 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer8.AddGrowableCol( 0 )
		fgSizer8.AddGrowableRow( 1 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer6 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Nix!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer6.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.filepicker_source = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		fgSizer6.Add( self.filepicker_source, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer8.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		m_checkList1Choices = [ u"Wee", u"Zee" ];
		self.m_checkList1 = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList1Choices, 0 )
		fgSizer8.Add( self.m_checkList1, 0, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer4.Add( fgSizer8, 1, wx.EXPAND, 5 )
		
		fgSizer4.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer4 )
		self.Layout()
	
	def __del__( self ):
		pass
	

