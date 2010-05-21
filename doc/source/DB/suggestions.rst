Verbesserungsvorschläge
=======================
Hier stehen Überlegungen zum Datenbank-Teil des Frameworks.


Neue Features
-------------
Wenn zwei Datenbanken miteinander synchronisiert werden sollen, werden
Hilfstabellen wichtig, besonders wenn nicht alle Datensätze Zeitstempel
enthalten. Dem soll über ein neues Modul namens ``SyncTools`` Rechnung
getragen werden. Mit Hilfe dieses Moduls soll folgendes möglich werden:
 - einfache Hilfstabellen anlegen, die einen Zeitstempel für das Datum der letzten
synchronisation enthalten. 


Abgehakt
--------
SQL Datenbanken geben zum aktuellen Stand bei einem ``SELECT`` die Daten in 
Form von `List of Dictionarys` (im folgenden `LODs` genannt) zurück. Leider 
müssen gegenwärtig (v0.1) die SQL-Befehle zum Schreiben jedes mal mühsam 
definiert werden. Ändern würde sich dieser Umstand, wenn dieselben `LODs`, 
welche ein ``SELECT`` zurückgibt, auch mit Hilfe einer Funktion geschrieben 
werden könnten. Folgende Transaktionen sind prärelevant:
 
 - ``INSERT`` Um Daten einzufügen.
 
 - ``UPDATE`` Um Daten zu ändern.
