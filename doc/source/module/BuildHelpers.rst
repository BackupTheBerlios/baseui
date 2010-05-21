:mod:`BuildHelpers` --- Tools zur Kompilierung
==============================================

.. module:: BuildHelpers
   :synopsis: Tools zur Kompilierung
   

BaseUI ist ein Framework, welches auch für die Erstellung von Distributionen 
Hilfsmittel zur Verfügung stellt. Das vorliegende Modul erledigt immer wieder 
kehrende Aufgaben, die beim Kompilieren einer Applikation auszuführen sind. 
Dabei werden in der vorliegenden Version folgende Pakete unterstützt:
 * GTK - Grafische Oberfläche
 * NSIS - Installer-Toolkit
 * SVN - Versionskontrolle
 * Sphinx - Dokumentations-Toolkit
 * SVG Grafik für das Startlogo
 

.. function:: get_winGTKdir()

   Diese Funktion bedient sich der Windows-Registry, um den Pfad der GTK 
   Installation als ``str`` zurückzugeben.
   
   
.. function:: get_nsi(*args, **kwargs)

   Der Installer NSIS benötigt ein Installer-Skript um ein Installationspaket 
   zu erstellen. Diese Funktion enthält ein Template für ein 
   Standard-Installations-Skript, welches mit den gegebenen Argumenten dieser 
   Funktion befüllt wird. Folgende Argumente werden berücksichtigt:
    * APP_NAME = Name der Applikation
    * APP_VERSION = Version der Applikation


.. function:: get_revision()

   Wenn das Paket ``pysvn`` installiert ist, gibt diese Funktion die 
   Revisionsnummer der SVN-Repository zurück.
   
   
.. function:: makeGTK(gtk_dir, pathname, build_dic, localized=False)
   
   Kopiert alle relevanten Dateien und Bibliotheken einer GTK-Installation, um 
   das eigenständige ausführen kompilierter GTK-Applikationen ohne GTK-Runtime 
   Installation zu ermöglichen. *gtk_dir* ist dabei der Pfad zur 
   GTK-Installation, *pathname* ist das Wurzelverzeichnis der zu kompilierenden 
   Applikation, *build_dir* ist der relative Pfad zum build-Verzeichnis und 
   *localized* stößt das Mitkopieren der zur Internationalisierung 
   erforderlichen Übersetzungsdateien mit, wenn ``True``.
 
 
.. function:: makeAbout(tpl_path, svg_path, author, version, revision, license)

   Diese Funktion befüllt die mit *tpl_path* angegebene SVG-Template-Datei 
   (z.B. für das Titelbild der Applikation) mit Daten und erstellt daraus eine 
   SVG-Grafik, deren Pfad und Name mit *svg_path* bestimmt wird.
   
   *author* ist der Name des Autors, *version* ist die Version der Applikation, 
   *revision* ist der SVN-Revisionsstand der Applikation und *license* gibt die 
   Lizenz der Applikation an. 
 
 
.. function:: makeNSI(pathname, build_dir, app_name, app_version)

   Um ein Installationspaket inklusive Uninstaller zu erstellen, müssen alle zu 
   installierenden Dateien ermittelt werden. Diese Funktion ruft die bereits 
   behandelte Funktion ``get_nsi`` auf, welche das Template für ein 
   NSI-Installationsskript erstellt.

   Das Argument *pathname* enthält das Wurzelverzeichnis der zu kompilierenden 
   Applikation, *build_dir* enthält den relativen Pfad zum build-Verzeichnis, 
   *app_name* steht für den Namen der Applikation und *app_version* ist die 
   gegenwärtige Version der Applikation.
 
 