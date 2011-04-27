# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi Definitions module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

data_types_lod = \
[
    {'id':  0, 'data_type': 'bool',      'description': {'DE': 'Binär'}},
    {'id':  1, 'data_type': 'int',       'description': {'DE': 'Ganzzahl'}},
    {'id':  2, 'data_type': 'float',     'description': {'DE': 'Fließkomma'}},
    {'id':  3, 'data_type': 'numeric',   'description': {'DE': 'Numerisch, frei definierbar'},   'arguments': '(%(numeric_scale)i, %(numeric_precision)i)'},
    {'id':  4, 'data_type': 'char',      'description': {'DE': 'Zeichenkette mit fester Länge'}, 'arguments': '(%(character_maximum_length)i)'},
    {'id':  5, 'data_type': 'varchar',   'description': {'DE': 'Zeichenkette variabler Länge'},  'arguments': '(%(character_maximum_length)i)'},
    {'id':  6, 'data_type': 'text',      'description': {'DE': 'Text beliebiger Länge'}},
    {'id':  7, 'data_type': 'time',      'description': {'DE': 'Zeit'}},
    {'id':  8, 'data_type': 'date',      'description': {'DE': 'Datum'}},
    {'id':  9, 'data_type': 'timestamp', 'description': {'DE': 'Zeitstempel (Datum und Zeit)'}},
]
