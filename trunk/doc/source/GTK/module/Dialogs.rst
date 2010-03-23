:mod:`Dialogs` --- Dialogfenster
================================

.. module:: Dialogs
   :synopsis: Dialogfenster
   
Vereinfachter Aufruf von PyGTK-Dialogen.

.. class:: Module

.. method:: Module.get_path()

   Liefert den Pfad, in dem sich GTKapi befindet. Diese Methode wird intern verwendet,
   um die Bilder für die Dialogboxen zu finden.
   

Einfache Dialogbox
------------------   
.. class:: Simple(parent=None)

   Liefert einfache Dialogboxen wie Infos, Ok/Abbruch-Fragen oder Fehlermeldungen. Das
   Attribut ``parent`` ist das Objekt des Fensters, das den Dialog aufruft. Es ist
   zwar nicht notwendig es anzugeben, es sorgt jedoch automatisch dafür, dass der
   Dialog im Vordergrund erscheint.
   

.. method:: Simple.show(dialog_type='info', title='Info', text='')

   ``dialog_type`` kann folgende Werte haben:
    - 'error' - Erzeugt eine Dialogbox für Fehlermeldungen mit einem 'Ok-Button' und Fehlersymbol.
    - 'question - Erzeugt eine Dialogbox mit zwei Buttons für 'Ok' und 'Abbruch' und Fragesymbol.
    - 'info' - Erzeugt eine Dialogbox mit einem 'Ok-Button' und einem Infosymbol.
   
   ``title`` ist ein string mit dem Fenstertitel des Dialogs
   
   ``text`` ist ein string mit dem Text des Dialoges.
   

   
Dateiauswahl Dialog
-------------------
.. class:: FileSelection(parent=None)

   Diese Klasse initiiert einen Dateiauswahldialog. Das Attribut ``parent`` ist das Objekt des
   Fensters, das den Dialog aufruft. 
   

.. method:: FileSelection.show(dialog_type='open', title='')

   ``dialog_type`` kann folgende Werte haben:
    - 'open' - Erzeugt eine Dateiauswahldialog zum öffnen von Dateien.
    - 'save - Erzeugt eine Dateiauswahldialog zum speichern von Dateien.
    - 'create folder' - Erzeugt eine Dateiauswahldialog zum erstellen von Verzeichnissen.
    - 'select folder' - Erzeugt eine Dateiauswahldialog zum auswählen von Verzeichnissen.
   
   ``title`` ist ein string mit dem Fenstertitel des Dialogs
   
   

Start-Dialog (splash-screen)
----------------------------
.. class:: Start

   Erstellt ein Objekt für einen splash-screen, wie er beim Start vieler Applikationen
   angezeigt wird.
   
   
.. method:: Start.show(start_image=None)

   ``start_image`` ist der Pfad des Bildes, welches der Splash-Screen anzeigen soll.
   
   
.. method:: Start.close()

   Schließt den Splash-Screen.
   
   
   