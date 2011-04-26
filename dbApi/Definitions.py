# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi Definitions module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

data_types_lod = \
[
    {'id':  0, 'data_type': 'bool',      'description': {'DE': 'Bin�r'}},
    {'id':  1, 'data_type': 'int',       'description': {'DE': 'Ganzzahl'}},
    {'id':  2, 'data_type': 'float',     'description': {'DE': 'Flie�komma'}},
    {'id':  3, 'data_type': 'numeric',   'description': {'DE': 'Numerisch, frei definierbar'},   'arguments': '(%(numeric_scale)i, %(numeric_precision)i)'},
    {'id':  4, 'data_type': 'char',      'description': {'DE': 'Zeichenkette mit fester L�nge'}, 'arguments': '(%(character_maximum_length)i)'},
    {'id':  5, 'data_type': 'varchar',   'description': {'DE': 'Zeichenkette variabler L�nge'},  'arguments': '(%(character_maximum_length)i)'},
    {'id':  6, 'data_type': 'text',      'description': {'DE': 'Text beliebiger L�nge'}},
    {'id':  7, 'data_type': 'time',      'description': {'DE': 'Zeit'}},
    {'id':  8, 'data_type': 'date',      'description': {'DE': 'Datum'}},
    {'id':  9, 'data_type': 'timestamp', 'description': {'DE': 'Zeitstempel (Datum und Zeit)'}},
]
