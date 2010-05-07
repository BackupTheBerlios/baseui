Einführung
==========
BaseUI ist das Ergebnis drei vorangegangener Entwicklungen. Diese lauten wie folgt:

 * ``GTKapi`` - Framework zur vereinfachten Benutzung von ``pyGTK``. Enthält auch kleine, eigene Tools die ausschließlich auf pyGTK basieren.
 
 * ``DBapi`` - Framework für standardisierten Datenbankzugriff auf alle üblichen SQL-Datenbanken.
 
 * ``PyCommons`` - Framework für den standardisierten Zugriff auf diverse Dateiformate und wiederkehrende Rechenaufgaben in Python.
 
Alle drei Module enthalten Teile, die gegenseitig benötigt werden. Prinzipiell ist ``BaseUI`` nur ein Modul, welches alle drei Frameworks beinhaltet. Dadurch ist es möglich, daß die übergreifenden Funktionen die Integrität der einzelnen Frameworks nicht vermindern. Es bleibt klar geregelt, welches Framework für welche Aufgabe steht. Gute Beispiele für übergreifende Funktionen sind z.B. Datenbank-Login, Datenbank-Tabellen oder ein Excel-Export einer Datenbanktabelle. Es werden für solche Funktionen gleichsam eine grafische Benutzeroberfläche benötigt, wie auch ein Datenbankzugriff. Durch das Überordnen des Elternmoduls ``BaseUI`` können die enthaltenen drei - nun untergeordneten Frameworks - um deren Uraufgabe kümmern ohne unübersichtlichen Ballast anzuhäufen. So bleibt der Code leserlich und gut gegliedert, ohne an Funktionalität zu verlieren. Auf der anderen Seite wird dadurch auch vermieden, dass die späteren Applikationen zuviel Code enthalten, der sich immer wiederholt. Auf diesem Wege werden auch Bugfixes im Framework sofort für alle Applikationen gültig.
