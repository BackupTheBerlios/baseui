class Tree:
    ''' Data Tree which is compatible to GTK.DataViews.Tree '''
    
    def __init__(self, tree_lod=None):
        ''' tree_lod is a list of dictionarys which has to have like this:
        
        tree_lod = \
        [
            {'name': 'Erfassung',   'picture': RESOURCE_DIR + "report_32.png"},
            {'name': 'Flugleitung', 'picture': RESOURCE_DIR + "tower_32.png"},            
            {'name': 'Stammdaten',  'picture': RESOURCE_DIR + "folder_32.png", '#child':
            [
                {'name': 'Personen',  'picture': RESOURCE_DIR + "member_32.png"},
                {'name': 'Flugzeuge', 'picture': RESOURCE_DIR + "aircraft_32.png"},
                {'name': u'Gebühren', 'picture': RESOURCE_DIR + "euro_32.png"}
            ]},
            {'name': 'Vorgaben', 'picture': RESOURCE_DIR + "folder_32.png", '#child':
            [
                {'name': 'Benutzergruppen',  'picture': RESOURCE_DIR + "user_group_32.png"},
                {'name': 'Lizenzen',         'picture': RESOURCE_DIR + "certificate_32.png"},
                {'name': 'Flugarten',        'picture': RESOURCE_DIR + "flight_types_32.png"},
                {'name': 'Startarten',       'picture': RESOURCE_DIR + "start_32.png"},
                {'name': 'Flugsektoren',     'picture': RESOURCE_DIR + "sectors_32.png"}
            ]},
        ] '''
        
        self.tree_lod = tree_lod
        
    
    def create(self, base_dic):
        self.tree_lod = [base_dic]
        
        
    def insert_before(self, node_dic):
        pass
        
        
    def insert_after(self, node_dic):
        pass
        
        
    def insert_into(self, node_dic):
        pass
        
        
    