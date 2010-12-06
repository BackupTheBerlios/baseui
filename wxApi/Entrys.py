import wx

# boolean entry:    checkbox    (wx.Checkbox)
# text entry:       entry       (wx.TextCtrl)
# combobox entry:   combobox    (wx.Combobox)   => many to one

# child FormTable:  FormTable                   <= one to many
# correlation:      


# Many to One:
# MEHRERE Autos haben EINEN Halter.

# One to Many:
# EINE Person hat MEHRERE Telefonnummern.

# Many to Many:
# MEHRERE Karusselle haben MEHRERE Preise.

class Combobox(wx.Combobox):
    def __init__(self, parent):
        wx.Combobox.__init__(self, parent)
        