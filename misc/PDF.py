# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons PDF module, creates simple Reports using ReportLab
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from pprint import pprint


class FormTable:
    def __init__(self):
        self._nof_columns = 0
        self._nof_rows = 0
        self.store = []
        self.style = []
        self._row_cursor = 0

        
    def initialize(self, definition_lod=None):
        ''' Initializes a FormTable for ReportLab.

            definition_lod = [{'column_name': 'id',
                               'label': 'Primärschlüssel',
                               'column_number': 0,
                               'row_number': 0}]'''

        self.definition_lod = definition_lod                       

        # Get number of rows and columns
        for dic in self.definition_lod:
            if dic.has_key('column_number'):
                if dic['column_number'] > self._nof_columns:
                    self._nof_columns = dic['column_number']
            if dic.has_key('row_number'):
                if dic['row_number'] > self._nof_rows:
                    self._nof_rows = dic['row_number']
        self._nof_columns = self._nof_columns + 1
        self._nof_rows = self._nof_rows + 1

        # Make some style
        self.style.append(('LINEABOVE', (0,0), (-1,0),                1, colors.blue))
        self.style.append(('LINEBELOW', (0,2), (-1,self._nof_rows-1), 1, colors.blue))
        self.style.append(('FONT',      (0,0), (-1,self._nof_rows-1), 'Times-Bold'))
        self._row_cursor = self._nof_rows-1
        
        # Make tree or table header
        for row_number in xrange(self._nof_rows):
            self._row_list = []
            for column_number in xrange(self._nof_columns):
                label = ''
                for dic in self.definition_lod:
                    if dic['row_number'] == row_number:
                        if dic['column_number'] == column_number:
                            label = dic['label']
                self._row_list.append(label)
            self.store.append(self._row_list)
    
    
    def populate(self, content_lod):
        ''' See BaseUI.GTK.DataViews.Tree for details, same format for content_lod. ''' 
        
        self.content_lod = content_lod

        # Iterate over all rows of content, then scan them for child nodes.
        try:
            for row_dict in self.content_lod:
                self.build_store(row_dict=row_dict)
                self.style.append(('LINEBELOW', (0,self._row_cursor), (-1,self._row_cursor), 0.5, colors.black))
        except:
            raise  
        

    def build_store(self, row_dict):
        # Make empty list with the right number of entrys.
        row_content = []
        for dummy in xrange(self._nof_columns):
            row_content.append('')

        # Populate list by overwriting empty entries
        for column_dict in self.definition_lod:
            if row_dict.has_key(column_dict['column_name']):
                column_content = row_dict[column_dict['column_name']]
                row_content[column_dict['column_number']] = column_content
                
        if row_dict.has_key('#child'):
            # Get child content from node
            self.store.append(row_content)
            self._row_cursor += 1
            for node_dict in row_dict['#child']:
                self.build_store(node_dict)
        else:
            # If no more child nodes exist, append the content.
            self.store.append(row_content)
            self._row_cursor += 1
            

if __name__ == "__main__":  
    definition = \
        [
            {'column_name': 'id',           'label': 'Kennzeichen', 'column_number': 0, 'row_number': 0},
            {'column_name': 'pattern',      'label': 'Muster',      'column_number': 1, 'row_number': 0},
            {'column_name': 'pilot_name',   'label': 'Piloten',     'column_number': 0, 'row_number': 1},
            {'column_name': 'start_time',   'label': 'Start',       'column_number': 1, 'row_number': 2},
            {'column_name': 'start_loc',    'label': 'Startort',    'column_number': 2, 'row_number': 2},
            {'column_name': 'landing_time', 'label': 'Ldg.',        'column_number': 3, 'row_number': 2},
            {'column_name': 'landing_loc',  'label': 'Landeort',    'column_number': 4, 'row_number': 2},
            {'column_name': 'duration',     'label': 'Dauer',       'column_number': 5, 'row_number': 2}
        ]
                                                                                  
    content = \
        [
            {'id': '7781', 'pattern': 'Technam P91', '#child':
            [
                {'pilot_name': 'Mark Muzenhardt',  '#child': 
                    [
                    {'start_time': '10:00', 'start_loc': 'Seckendorf', 'landing_time': '11:00', 'landing_loc': 'Seckendorf', 'duration': '01:00'},
                    {'start_time': '12:00', 'start_loc': 'Seckendorf', 'landing_time': '13:00', 'landing_loc': 'Seckendorf', 'duration': '01:00'},
                    ]
                },
            ]},
            {'id': 'ERPL', 'pattern': 'Chessna', '#child':
            [
                {'pilot_name': 'Lukas Flor',  '#child': 
                    [
                    {'start_time': '10:00', 'start_loc': 'Seckendorf', 'landing_time': '11:00', 'landing_loc': 'Seckendorf', 'duration': '01:00'},
                    {'start_time': '12:00', 'start_loc': 'Seckendorf', 'landing_time': '13:00', 'landing_loc': 'Seckendorf', 'duration': '01:00'},
                    ]
                },
            ]},
        ]

    form_table = FormTable()
    form_table.initialize(definition_lod=definition)
    form_table.populate(content_lod=content)

    # Our container for 'Flowable' objects
    elements = []
     
    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
     
    # A basic document for us to write to 'rl_hello_table.pdf'
    doc = SimpleDocTemplate('test.pdf')
     
    elements.append(Paragraph("Konsens", styles['Title']))
      
    # Create the table with the necessary style, and add it to the
    # elements list.
    table = Table(form_table.store, style=form_table.style, repeatRows=form_table._nof_rows)
    elements.append(table)
     
    # Write the document to disk
    doc.build(elements)
    os.startfile('test.pdf')




