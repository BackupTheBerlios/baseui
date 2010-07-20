Einf�hrung
==========

F�r Python existieren Zahlreiche Datenbank-Konnektoren, die SQL kompatible Datenbanken verschiedener Hersteller an Python anbinden k�nnen. Fast alle namhaften Datenbank-Konnektoren entsprechen heute dem DB-API-2.0 Standard von Python. Trotzdem ist noch immer ein abweichendes Handling zu beobachten, das oft nicht dem Konnektor zuzuschreiben ist, sondern h�ufig dem unterschiedlichen Aufbau der Datenbanken selbst.

Oft ben�tigt wird zum Beispiel eine einheitliche M�glichkeit, die Tabellendefinitionen abzufragen. Ohne DBapi w�hre die Abfrage an die jeweilige Datenbank anzupassen. 

Ein weiteres, h�ufig ben�tigtes Feature ist die synchronisation des von einer Applikation verwendeten Datenbankmodells mit dem realen Datenbankmodell. Auch hierfuer bietet DBapi ein m�chtiges Tool an, welches verschiedene Synchronisationstiefen unterstuetzt.

DBapi ist ausdruecklich kein ORM (Objekt Rationaler Mapper). Stattdessen erwartet DBapi altgewohnten SQL-Code als Eingabe und gibt entweder Listen oder in Listen enthaltene Dictionarys zurueck. Die Vereinheitlichung der Datenbankbefehle erfolgt einfach mittels Funktionsaufruf, DBapi gibt dann die entsprechenden Befehle an die jeweilige Datenbank.
