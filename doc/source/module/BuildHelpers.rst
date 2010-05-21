:mod:`BuildHelpers` --- Tools zur Kompilierung
==============================================

.. module:: BuildHelpers
   :synopsis: Tools zur Kompilierung
   

BaseUI ist ein Framework, welches auch f�r die Erstellung von Distributionen 
Hilfsmittel zur Verf�gung stellt. Das vorliegende Modul erledigt immer wieder 
kehrende Aufgaben, die beim Kompilieren einer Applikation auszuf�hren sind. 
Dabei werden in der vorliegenden Version folgende Pakete unterst�tzt:
 * GTK - Grafische Oberfl�che
 * NSIS - Installer-Toolkit
 * SVN - Versionskontrolle
 * Sphinx - Dokumentations-Toolkit
 * SVG Grafik f�r das Startlogo
 

.. function:: get_winGTKdir()

   Diese Funktion bedient sich der Windows-Registry, um den Pfad der GTK 
   Installation als ``str`` zur�ckzugeben.
   
   
.. function:: get_nsi(*args, **kwargs)

   Der Installer NSIS ben�tigt ein Installer-Skript um ein Installationspaket 
   zu erstellen. Diese Funktion enth�lt ein Template f�r ein 
   Standard-Installations-Skript, welches mit den gegebenen Argumenten dieser 
   Funktion bef�llt wird. Folgende Argumente werden ber�cksichtigt:
    * APP_NAME = Name der Applikation
    * APP_VERSION = Version der Applikation


.. function:: get_revision()

   Wenn das Paket ``pysvn`` installiert ist, gibt diese Funktion die 
   Revisionsnummer der SVN-Repository zur�ck.
   
   
.. function:: makeGTK(gtk_dir, pathname, build_dic, localized=False)
   
   Kopiert alle relevanten Dateien und Bibliotheken einer GTK-Installation, um 
   das eigenst�ndige ausf�hren kompilierter GTK-Applikationen ohne GTK-Runtime 
   Installation zu erm�glichen. *gtk_dir* ist dabei der Pfad zur 
   GTK-Installation, *pathname* ist das Wurzelverzeichnis der zu kompilierenden 
   Applikation, *build_dir* ist der relative Pfad zum build-Verzeichnis und 
   *localized* st��t das Mitkopieren der zur Internationalisierung 
   erforderlichen �bersetzungsdateien mit, wenn ``True``.
 
 
.. function:: makeAbout(tpl_path, svg_path, author, version, revision, license)

   Diese Funktion bef�llt die mit *tpl_path* angegebene SVG-Template-Datei 
   (z.B. f�r das Titelbild der Applikation) mit Daten und erstellt daraus eine 
   SVG-Grafik, deren Pfad und Name mit *svg_path* bestimmt wird.
   
   *author* ist der Name des Autors, *version* ist die Version der Applikation, 
   *revision* ist der SVN-Revisionsstand der Applikation und *license* gibt die 
   Lizenz der Applikation an. 
 
 
.. function:: makeNSI(pathname, build_dir, app_name, app_version)

   Um ein Installationspaket inklusive Uninstaller zu erstellen, m�ssen alle zu 
   installierenden Dateien ermittelt werden. Diese Funktion ruft die bereits 
   behandelte Funktion ``get_nsi`` auf, welche das Template f�r ein 
   NSI-Installationsskript erstellt.

   Das Argument *pathname* enth�lt das Wurzelverzeichnis der zu kompilierenden 
   Applikation, *build_dir* enth�lt den relativen Pfad zum build-Verzeichnis, 
   *app_name* steht f�r den Namen der Applikation und *app_version* ist die 
   gegenw�rtige Version der Applikation.
 
 