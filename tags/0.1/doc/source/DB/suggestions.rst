Verbesserungsvorschläge
=======================

SQL Datenbanken geben zum aktuellen Stand bei einem ``SELECT`` die Daten in Form von `List of Dictionarys` (im folgenden `LODs` genannt) zurück. Leider müssen gegenwärtig (v0.1) die SQL-Befehle zum Schreiben jedes mal mühsam definiert werden. Ändern würde sich dieser Umstand, wenn dieselben `LODs`, welche ein ``SELECT`` zurückgibt, auch mit Hilfe einer Funktion geschrieben werden könnten. Folgende Transaktionen sind prärelevant:
 
 - ``INSERT`` Um Daten einzufügen.
 
 - ``UPDATE`` Um Daten zu ändern.
 