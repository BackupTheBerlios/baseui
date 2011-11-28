Roadmap
=======
Die Entwicklungslinie und �nderungsanzeigen sowie ToDo-Liste.


Version 0.1
-----------
 - Import der Frameworks ``GTKapi``, ``PyCommons`` und ``DBapi``.
 - Umbenennen der importierten Frameworks in: ``GTK``, ``Commons`` und ``DB``.
 - L�schantrag f�r die alten Framework-Schnipsel.
 - BerliOS-Antrag auf neues Projekt ``BaseUI``.
 - Ver�ffentlichung von Version 0.1 mit Precompiled Package f�r Windows.
 

Version 2.0
-----------
Nachdem nun einige Applikationen mit BaseUI realisiert wurden ist es an der Zeit,
alten Ballast loszuwerden bevor neue Projekte realisiert werden. Vor allem diese
Belange sollen angegangen werden:
 - eigene Encodings f�r die unterschiedlichen Datenbanken zulassen (bis jetzt
   ist alles auf msSQL �ber ODBC ausgelegt!)
 - eigene Transformations-Algorithmen f�r die unterschiedlichen Datenbanken
   zulassen (bis jetzt werden alle DBs gleich transformiert, was nicht tragbar 
   ist!)
   
Aus vergangenen Applikationen konnte gelernt werden, dass verschiedene Dialoge
immer wieder gebraucht werden:
 - einfacher INI-Konfigurationsdialog
 - Tabelle f�r JSON-Daten
 - Dialog f�r Tabs mit Formular-Panels
 
Die Datenauskunft ist stark verbesserungsbed�rftig. An diesen Dingen hakts:
 - Formulardruck, erfordert mindestens 'label'-Attribut in vorhandene Formularen,
   zudem wird die �bersetzbarkeit mit diesem Attribut erst m�glich!
 - Standardexport von Excel-Tabellen aus einer vorhandenen Datentabelle
 - Tabellendruck von Datentabellen

 
Version 3.0
-----------
Drucken aus Formularen ist allerdings kein triviales Problem. Daf�r sind mindestens
auch die Koordinaten der Felder auf dem Report anzugeben. Hier kommt wieder die
gute, alte Forderung nach einem Report-Editor zu Tage. 


Version 4.0
-----------
- Die Darstellung korrekter SVG-Grafiken w�re ein erstrebenswertes Ziel.
- Datenbank-Administrations-Tool ist neben Report-Tool nat�rlich phat.
- Der Python-Server k�nnte eine BaseUI-App werden!
