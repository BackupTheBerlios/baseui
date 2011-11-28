Roadmap
=======
Die Entwicklungslinie und Änderungsanzeigen sowie ToDo-Liste.


Version 0.1
-----------
 - Import der Frameworks ``GTKapi``, ``PyCommons`` und ``DBapi``.
 - Umbenennen der importierten Frameworks in: ``GTK``, ``Commons`` und ``DB``.
 - Löschantrag für die alten Framework-Schnipsel.
 - BerliOS-Antrag auf neues Projekt ``BaseUI``.
 - Veröffentlichung von Version 0.1 mit Precompiled Package für Windows.
 

Version 2.0
-----------
Nachdem nun einige Applikationen mit BaseUI realisiert wurden ist es an der Zeit,
alten Ballast loszuwerden bevor neue Projekte realisiert werden. Vor allem diese
Belange sollen angegangen werden:
 - eigene Encodings für die unterschiedlichen Datenbanken zulassen (bis jetzt
   ist alles auf msSQL über ODBC ausgelegt!)
 - eigene Transformations-Algorithmen für die unterschiedlichen Datenbanken
   zulassen (bis jetzt werden alle DBs gleich transformiert, was nicht tragbar 
   ist!)
   
Aus vergangenen Applikationen konnte gelernt werden, dass verschiedene Dialoge
immer wieder gebraucht werden:
 - einfacher INI-Konfigurationsdialog
 - Tabelle für JSON-Daten
 - Dialog für Tabs mit Formular-Panels
 
Die Datenauskunft ist stark verbesserungsbedürftig. An diesen Dingen hakts:
 - Formulardruck, erfordert mindestens 'label'-Attribut in vorhandene Formularen,
   zudem wird die übersetzbarkeit mit diesem Attribut erst möglich!
 - Standardexport von Excel-Tabellen aus einer vorhandenen Datentabelle
 - Tabellendruck von Datentabellen

 
Version 3.0
-----------
Drucken aus Formularen ist allerdings kein triviales Problem. Dafür sind mindestens
auch die Koordinaten der Felder auf dem Report anzugeben. Hier kommt wieder die
gute, alte Forderung nach einem Report-Editor zu Tage. 


Version 4.0
-----------
- Die Darstellung korrekter SVG-Grafiken wäre ein erstrebenswertes Ziel.
- Datenbank-Administrations-Tool ist neben Report-Tool natürlich phat.
- Der Python-Server könnte eine BaseUI-App werden!
