:mod:`FileSystem` --- Zugriff auf verschiedene Dateiformate
===========================================================

.. module:: FileSystem
   :synopsis: Zugriff auf verschiedene Dateiformate

Dieses Modul bietet Zugriff auf verschiedene Dateiformate.



:class:`iniFile` --- Zugriff auf .ini-Dateien
---------------------------------------------

.ini-Dateien stellen ein sehr einfaches Format zur Verf�gung, um Konfigurationsdaten in einer Datei ablegen zu k�nnen.

.. class:: iniFile(filename)

   Erstellt ein Objekt, mit dem .ini-Dateien verarbeitet werden k�nnen.
   
   
.. method:: iniFile.dictresult(section)

   Gibt ein ``list_of_dictionarys`` zur�ck, das die Schl�ssel und Werte der .ini-Datei enth�lt.
   
   
.. method:: iniFile.save(ini_text)

   Diese Methode ist nur eine Vereinfachung, um den Inhalt einer .ini-Datei schreiben zu k�nnen. Das Attribut ``ini_text`` beinhaltet einfach nur einen String, der den Inhalt der .ini-Datei repr�sentiert.



:class:`xlsFile` --- Zugriff auf Excel-Dateien
----------------------------------------------

.. class:: xlsFile(filename, encoding='cp1251')

   Erstellt das Objekt einer Excel-Datei.

   
   
:class:`csvFile` --- Zugriff auf .csv-Dateien
---------------------------------------------

.csv-Dateien stellen ein sehr einfaches Format bereit, mit dessen Hilfe Tabellen in einer Datei abgelegt werden k�nnen. Die Python-Standard-Bibliothek stellt bereits Methoden zur Verf�gung, um diese Dateien verarbeiten zu k�nnen. Diese Klasse standardisiert die Ein- und Ausgabe der Daten, um diese auch in andere Dateiformate (z.B. Excel) �bertragen zu k�nnen. 

.. class:: xlsFile(filename, encoding='cp1251')

   Erstellt das Objekt einer .csv-Datei.