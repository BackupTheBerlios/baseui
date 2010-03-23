Verbesserungsvorschl�ge
=======================

SQL Datenbanken geben zum aktuellen Stand bei einem ``SELECT`` die Daten in Form von `List of Dictionarys` (im folgenden `LODs` genannt) zur�ck. Leider m�ssen gegenw�rtig (v0.1) die SQL-Befehle zum Schreiben jedes mal m�hsam definiert werden. �ndern w�rde sich dieser Umstand, wenn dieselben `LODs`, welche ein ``SELECT`` zur�ckgibt, auch mit Hilfe einer Funktion geschrieben werden k�nnten. Folgende Transaktionen sind pr�relevant:
 
 - ``INSERT`` Um Daten einzuf�gen.
 
 - ``UPDATE`` Um Daten zu �ndern.
 