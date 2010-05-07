:mod:`Portlets` --- Portlets für den Datenbankzugriff
=====================================================

.. module:: Portlets
   :synopsis:  Portlets für den Datenbankzugriff
   
Bei Datenbankapplikationen kommen immer wieder ähnliche Problemstellungen auf 
den Programmierer zu. BaseUI trennt die Datenbankoperationen grundsätzlich von 
den Anzeigeoperationen. Da aber Tabellen und Formulare stets Datenbankinhalt 
verarbeiten müssen, verbindet dieses Modul die Datenbank mit der Ausgabe. 
Grundsätzlich soll Datenbankinhalt immer mit Hilfe von Tabellen dargestellt 
werden. Wird eine Tabellenzeile angewählt, so sollte sich meist ein Formular 
öffnen, in welchem der gewählte Datensatz bearbeitet werden kann.
   

.. class:: DatabaseLogin

   Nicht dokumentiert.
   
   .. function:: __init__(self, ini_filename='', autosave=False, parent=None)

      Nicht dokumentiert.
      
      
      
.. class:: UserLogin

   Nicht dokumentiert.
   
   .. function:: __init__(self, content_lod=[], merge_field_list=[], parent=None)

      Nicht dokumentiert.
      
      
      
.. class:: ftpLogin

   Nicht dokumentiert.
   
   .. function:: __init__(self, ini_filename=[], autosave=False, parent=None)

      Nicht dokumentiert.
      
            

.. class:: Table

   Nicht dokumentiert.
   
   .. function:: __init__(self, form_object=None, parent_form=None, dataset=True, report=False, search=False, filter=True, help=True, db_table=None, help_file=None, separate_toolbar=True)

      Nicht dokumentiert.
      
      
      
.. class:: Form

   Nicht dokumentiert.
   
   .. function:: __init__(self, parent_form=None, icon_file=None, title=None, glade_file=None, window_name=None, help_file=None)

      Nicht dokumentiert.
      

      
.. class:: Serial

   Nicht dokumentiert.
   
   .. function:: __init__(self)

      Nicht dokumentiert.