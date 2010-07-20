Einführung
==========

Für Python existieren Zahlreiche Datenbank-Konnektoren, die SQL kompatible Datenbanken verschiedener Hersteller an Python anbinden können. Fast alle namhaften Datenbank-Konnektoren entsprechen heute dem DB-API-2.0 Standard von Python. Trotzdem ist noch immer ein abweichendes Handling zu beobachten, das oft nicht dem Konnektor zuzuschreiben ist, sondern häufig dem unterschiedlichen Aufbau der Datenbanken selbst.

Oft benötigt wird zum Beispiel eine einheitliche Möglichkeit, die Tabellendefinitionen abzufragen. Ohne DBapi währe die Abfrage an die jeweilige Datenbank anzupassen. 

Ein weiteres, häufig benötigtes Feature ist die synchronisation des von einer Applikation verwendeten Datenbankmodells mit dem realen Datenbankmodell. Auch hierfuer bietet DBapi ein mächtiges Tool an, welches verschiedene Synchronisationstiefen unterstuetzt.

DBapi ist ausdruecklich kein ORM (Objekt Rationaler Mapper). Stattdessen erwartet DBapi altgewohnten SQL-Code als Eingabe und gibt entweder Listen oder in Listen enthaltene Dictionarys zurueck. Die Vereinheitlichung der Datenbankbefehle erfolgt einfach mittels Funktionsaufruf, DBapi gibt dann die entsprechenden Befehle an die jeweilige Datenbank.
