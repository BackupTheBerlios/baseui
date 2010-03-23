:mod:`DataViews` --- Datensichtungen
====================================

.. module:: DataViews
   :synopsis: Datensichtungen
   
Datensichtungen können Tabellen, Baumansichten, Formulare oder Reports sein. Wichtig ist, daß die Datenströme bei allen Ansichten auf ein möglichst einheitliches Datenaustauschformat setzen, das JSON ähnelt und leicht umzusetzen ist. Ebenfalls erwähnenswert ist, dass dieses Modul besonders gut mit dem Python-Modul ``DBapi`` zusammenarbeitet, welches die Daten gleich im richtigen Format liefert.

Wenn möglich, beschränkt sich dieses Modul auf die sogenannten `list of dictionarys`, welches entweder die Spaltenkonfiguration oder den Inhalt einer Tabelle (oder eines Baumes) enthält. 


Tabellen- und Baumansicht
-------------------------

.. class:: Tree(widget=None)

   Die Benutzung von PyGTK Tabellen wird vereinfacht durch Festlegung eines Datenaustauschformats, 
   das JSON ähnlich ist. Das Attribut ´´widget´´ ist ein ´´gtk.TreeView´´ Objekt.

   
.. method:: Tree.on_column_toggled(renderer=None, row=None, widget=None, col=None)

   Diese Methode wird intern für das umschalten der ToggleRenderer in einer Spalte 
   des Datentyps ´´bool´´ benötigt. 
   

.. method:: Tree.compare_by(fieldname)

   Wird intern verwendet, um Dictionarys sortieren zu können.
   
   .. method:: Tree.compare_by.compare_two_dicts(a, b)
   
   Siehe Elternmethode.
   
   
.. method:: Tree.clear()

   Löscht den Inhalt der Ansicht, indem alle Spalten aufgelöst werden.
   
.. method:: Tree.initialize(table_definition_lod)

   Bevor die Tabelle mit Daten befüllt werden kann, müssen die Eigenschaften der Spalten
   definiert werden. Dies geschieht mittels einer 'list of dictionarys'.
   
   Beispiel::
   
      table_definition_lod = [{'column_name': 'id',
                               'data_type': 'bigint',

                               'column_label': 'Primärschlüssel',
                               'column_number': 0,

                               'visible': True,
                               'editable': True,
                               'sortable': True,
                               'resizeable': True,
                               'reorderable': True}]
                                 
 
.. method:: Tree.populate(table_content_lod)

   Diese Methode befüllt die Tabelle mit den Daten, die im ´´table_content_lod´´
   definiert sind. Es handelt sich um ein 'list of dictionarys', welches die Zeilen
   der Tabelle beinhaltet.
   
   Beispiel::
   
      table_content_lod = [{'id': 1}]
   
   
.. method:: Tree.build_store(row_parent, row_dict)

   Wird intern verwandt, um auch Baumansichten generieren zu können.


.. method:: Tree.build_definition(table_content_lod, column_list=None)

   Wenn die Eigenschaften der Spalten abhängig von deren Dateninhalt definiert werden
   müssen, kann dies mit Hilfe dieser Methode bewerkstelligt werden. Das ´´table_content_lod´´
   ist wieder ein 'list of dictionarys', das die Zeilen der Tabelle definiert. Das
   Attribut ´´column_list´´ ist vorgesehen, um die gewünschten Spalten auswählen zu können.
   
                                     
.. method:: Tree.set_sort_column(sort_column=0, sort_ascending=True)

   Wenn eine Tabelle nach einer Spalte sortiert werden soll, kann diese mit dieser Methode
   ausgewählt werden. ´´sort_column´´ ist dabei die Spaltennummer, das Attribut
   ´´sort_ascending´´ gibt die Sortierreihenfolge an, welche bei ´´True´´ aufsteigend ist.
   
   
.. method:: Tree.sort_liststore(column):

   Kommt noch...

   
Benutzung::  
        
    table_definition_lod = [
                           {'column_name': 'name',
                                'data_type': 'varchar',

                                'column_label': 'Name',
                                'column_number': 1,
                                'visible': True,
                                'editable': True,
                                'sortable': True,
                                'resizeable': True,
                                'reorderable': True,
                                'expand': True},
                            {'column_name': 'has_phone',
                                'data_type': 'bool',

                                'column_label': 'Hat Telefon?',
                                'column_number': 2,
                                'visible': True,
                                'editable': False,
                                'sortable': True},
                            {'column_name': 'has_car',
                                'data_type': 'bool',

                                'column_label': 'Hat Auto?',
                                'column_number': 3,
                                'visible': True,
                                'editable': True,
                                'sortable': True,
                                'visible': True},
                           {'column_name': 'picture',
                                'data_type': 'image',

                                'column_label': 'Bild',
                                'column_number': 0,
                                'visible': True,
                                'editable': False,
                                'visible': True}
                           ]

    table_content_lod = [
                        {'name': 'Herbert', 'picture': RESOURCE_DIR + 'folder-open_16.png', 'has_phone': False, 'has_car': True, 'child':
                            [
                            {'name': 'Heinz', 'has_phone': True, 'picture': RESOURCE_DIR + 'database_16.png'}
                            ]
                        },
                        {'name': 'Hugo', 'picture': RESOURCE_DIR + 'database_16.png'},
                        {'name': 'Hubert', 'picture': RESOURCE_DIR + 'folder-open_16.png', 'has_phone': True, 'child':
                            [
                            {'name': 'Simon', 'picture': RESOURCE_DIR + 'folder-open_16.png', 'child':
                               [
                               {'name': 'Balduin', 'picture': RESOURCE_DIR + 'database_16.png'},
                               {'name': 'Detlef', 'picture': RESOURCE_DIR + 'database_16.png'} 
                               ]
                            },
                            {'name': 'Markus', 'picture': RESOURCE_DIR + 'database_16.png', 'has_car': True},
                            {'name': 'Marco', 'picture': RESOURCE_DIR + 'folder-open_16.png', 'child':
                                [
                                {'name': 'Heidi', 'picture': RESOURCE_DIR + 'database_16.png'},
                                {'name': 'Gert', 'picture': RESOURCE_DIR + 'database_16.png'},
                                {'name': 'Klaus', 'picture': RESOURCE_DIR + 'database_16.png'}
                                ]
                            }
                            ]
                        }
                        ]

    TableLeft = Widgets.Table(self.treeview_left)
    
    TableLeft.initialize(table_definition_lod)
    TableLeft.populate(table_content_lod)
    TableLeft.set_sort_column(1)
    

Form Brain wrapping
-------------------

Hier ist notwendig, dass es mindestens eine widget definition gibt. Irgendwie
müssen ja die Daten aus einer Datenbank-Tabelle die Felder der Formulars befüllen.


Report Brain wrapping
---------------------

Ein Report besteht aus mehreren Blättern DIN A4-Seiten. Dabei gibt es immer eine
Vorderseite, eine Folgeseite und eine letzte Seite. =>
- vielleicht ist es auch anders und man sollte eine Baumstruktur einführen?
- so könnte es sein: Dokument => Teil => Kapitel => Überschrift 1 => ...

Zumindest eine Seitendefinition ist unbedingt notwendig. Im Prinzip muss es folgede
Dinge geben:

 - Textfeld, 
 - Tabellenfeld
 - Linie, Polylinie => Rechteck, Polygon.
 - Kreis, Ellipse
 - Bilder
 - Formularfeld (für sich in den Feldern wiederholende Datenbankauskünfte)

Der Report besteht aus zwei Teilen:
 - Daten-Container,
    => Womit ist das Formular eigentlich ausgefüllt?

 - Repräsentations-Definition.
    => Wo sollen die Daten eigentlich auf dem Papier stehen?
