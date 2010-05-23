:mod:`Transformations` --- Transformation zwischen Python und SQL
=================================================================

.. module:: Transformations
   :synopsis:  Transformation zwischen Python und SQL
   

Nicht dokuentiert.
   
   
 
.. function:: DataType_to_SQL(data_type, mssql=False, oracle=False, length=40)

   Transformiert den Python-Datentyp ``data_type`` zu einem SQL-Datentyp. Da
   die Datenbanken `mssql` und `oracle` �ber eigene Gesetze verf�gen (was die
   Namen der Datentypen betrifft), gibt es die beiden gleichnamigen Schalter.
   
   
.. function:: write_transform(content, engine)

   Wenn Inhalte in eine Datenbank geschrieben werden sollen, variieren die
   Erwartungen der Datenbankhersteller bez�glich des Datenformats. Diese
   Funktion ist einer jeden Schreiboperation vorgeschaltet, die auf eine
   Tabelle angewendet wird. 
   
   
.. function:: normalize_content(attributes_lod, content_lod)

   Diese Funktion sollte eigentlich read_transform heissen. Sie normalisiert
   den Datenbank-Output so, dass vern�nftige Werte in den korrekten Datentypen
   abgelegt werden. Das ``attributes_lod`` wird ben�tigt, um die Inhalte des
   ``content_lod`` transformieren zu k�nnen.
   
   
   