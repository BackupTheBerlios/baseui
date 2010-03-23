:mod:`SQLdb` --- SQL-Datenbankzugriff
=====================================

.. module:: SQLdb
   :synopsis: SQL-Datenbankzugriff.
   

.. function:: get_engines()
   
   Gibt eine Liste der verf�gbaren Datenbank-Konnektoren zur�ck. M�glich sind folgende Zeichenketten:
    - MySQL
    - PostgreSQL
    - msSQL
    - SQLlite
    - Oracle
.. note:: Die zur�ckgegebene Liste enth�lt die Datenbankbezeichnungen im richtigen Format f�r die Initialisierung der Klasse :class:`database`.

 
:class:`database` --- Datenbankzugriff
--------------------------------------

.. class:: database

   Erstellt ein Datenbank-Objekt, das den Cursor und die eigentliche Datenbank-Verbindung beinhaltet.

.. attribute:: database.engine 
    
   Zeichenkette mit folgenden, m�glichen Werten: 
    - MySQL
    - PostgreSQL
    - msSQL
    - SQLlite
    - Oracle
   
.. attribute:: database.encoding

   Das Attribut :attr:`database.encoding` legt die Zeichenkodierung der Datenbank fest. Es ist nur erforderlich, wenn eine neue Datenbank angelegt wird. 

.. attribute:: database.connector

   Der Datenbank-Konnektor wird �bergeladen in dieses Attribut.
 
.. method:: database.__init__(engine, encoding)
   
   Initialisiert die Klasse :class:`database`. Das Attribut :attr:`engine` ist eine Zeichenkette mit folgenden, m�glichen Werten:

   
   
 
 
.. method:: database.connect(**kwargs)

   Mit dieser Methode wird die Datenbank verbunden. Folgende Argumente werden erwartet:
  
   .. data:: database 
       
      Datenbankname. Bei SQLite ist dies der Dateiname der zu �ffnenden Datenbank.
         
   .. data:: host
       
      Hostname des Datenbankservers. Bei Abweichen vom Standard-Port ist dieser mit Doppelpunkt anzuh�ngen. Bei SQLite ist hier der lokale Pfad zur Datenbank-Datei anzugeben.
     
   .. data:: user
  
      Datenbank Benutzername. Nicht bei SQLite, da hier keine Benutzerverwaltung vorliegt.
     
   .. data:: password
  
      Passwort des Datenbank Benutzers. Ist ebenfalls nicht anzugeben bei SQLite.


.. method:: database.close()

   Die ge�ffnete Datenbankverbindung wird geschlossen, sobald diese Methode aufgerufen wird.
   
   
.. method:: database.create(database, encoding)

   Wenn eine Datenbankverbindung mit ausreichenden Benutzerrechten ge�ffnet ist, kann eine neue Datenbank erstellt werden. Das Attribut :attr:`database` ist eine Zeichenkette und steht f�r den Datenbanknamen, w�hrend :attr:`encoding` die Zeichenkodierung der neu zu erstellende Datenbank angibt.
   
   
.. method:: database.drop(database)

   Wenn der Benutzer der offenen Datenbankverbindung gen�gend Rechte besitzt, um eine Datenbank zu L�schen, kann mit dieser Methode die mit dem Attribut :attr:`database` angegebene Datenbank gel�scht werden.


.. method:: database.comit()

   Beim Aufruf dieser Methode werden alle offenen Transaktionen in der Warteliste der Datenbank ausgef�hrt. Wenn die verbundene Datenbank �ber eine autocommit-Funktion verf�gt, sollte :meth:`commit` nicht manuell aufgerufen werden.

   
.. method:: database.listresult(sql_command)
   
   Wenn eine Datenbankabfrage ihr Ergebnis als Liste zur�ckgeben soll, ist der SQL-Befehl mit Hilfe dieser Methode ausgef�hrt werden. Das Attribut :attr:`sql_command` ist eine Zeichenkette, die den SQL-Befehl beinhaltet.


.. method:: database.dictresult(sql_command)

   Wird das Ergebnis einer Datenbankabfrage in Form einer Liste von Dictionarys �bergeben werden soll, ist die SQL-Abfrage mit Hilfe dieser Methode auszuf�hren. Das Attribut :attr:`sql_command` ist eine Zeichenkette, die den SQL-Befehl beinhalten muss.


.. method:: database.get_tables

   Wenn abgefragt werden soll, welche Tabellen die gerade verbundene Datenbank enth�lt, ist :meth:`get_tables` aufzurufen. Das Ergebnis wird in Form einer Liste �bergeben, die Zeichenketten der Tabellennamen beinhaltet.


.. method:: database.get_users

   Diese Methode �bergibt eine Liste von Zeichenketten, die alle Benutzer der verbundenen Datenbank beinhaltet.
   
      

:class:`table` --- Tabellenzugriff
----------------------------------

.. class:: table
   
   Erstellt ein Tabellenobjekt.
   
   

:class:`user` --- Das Benutzerzugriff
-------------------------------------

.. class:: user

   Erstellt ein Benutzerobjekt.
   
