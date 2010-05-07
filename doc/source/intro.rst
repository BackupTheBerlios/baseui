Einf�hrung
==========
BaseUI ist das Ergebnis drei vorangegangener Entwicklungen. Diese lauten wie folgt:

 * ``GTKapi`` - Framework zur vereinfachten Benutzung von ``pyGTK``. Enth�lt auch kleine, eigene Tools die ausschlie�lich auf pyGTK basieren.
 
 * ``DBapi`` - Framework f�r standardisierten Datenbankzugriff auf alle �blichen SQL-Datenbanken.
 
 * ``PyCommons`` - Framework f�r den standardisierten Zugriff auf diverse Dateiformate und wiederkehrende Rechenaufgaben in Python.
 
Alle drei Module enthalten Teile, die gegenseitig ben�tigt werden. Prinzipiell ist ``BaseUI`` nur ein Modul, welches alle drei Frameworks beinhaltet. Dadurch ist es m�glich, da� die �bergreifenden Funktionen die Integrit�t der einzelnen Frameworks nicht vermindern. Es bleibt klar geregelt, welches Framework f�r welche Aufgabe steht. Gute Beispiele f�r �bergreifende Funktionen sind z.B. Datenbank-Login, Datenbank-Tabellen oder ein Excel-Export einer Datenbanktabelle. Es werden f�r solche Funktionen gleichsam eine grafische Benutzeroberfl�che ben�tigt, wie auch ein Datenbankzugriff. Durch das �berordnen des Elternmoduls ``BaseUI`` k�nnen die enthaltenen drei - nun untergeordneten Frameworks - um deren Uraufgabe k�mmern ohne un�bersichtlichen Ballast anzuh�ufen. So bleibt der Code leserlich und gut gegliedert, ohne an Funktionalit�t zu verlieren. Auf der anderen Seite wird dadurch auch vermieden, dass die sp�teren Applikationen zuviel Code enthalten, der sich immer wiederholt. Auf diesem Wege werden auch Bugfixes im Framework sofort f�r alle Applikationen g�ltig.
