import res.Portlets


class Database(res.Portlets.Database):
    def __init__(self, parent):
        res.Portlets.Database.__init__(self, parent)
        
        
        
class Login(res.Portlets.Login):
    def __init__(self, parent):
        res.Portlets.Login.__init__(self, parent)