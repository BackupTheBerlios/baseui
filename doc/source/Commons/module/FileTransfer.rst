:mod:`FileTransfer` --- Dateitransfer mittels FTP, etc.
=======================================================

.. module:: FileTransfer
   :synopsis: Dateitransfer mittels FTP, etc.

Dieses Modul beherbergt verschiedene Datenübertragungsformate, gegenwärtig nur
FTP. Künftig sollen noch andere Formate wie z.B. SCP folgen.



:class:`FTP` --- Zugriff auf FTP-Server
---------------------------------------

Diese Klasse steht für eine Verbindung zu einem FTP-Server. Es stellt immer
wieder kehrende Funktionen bereit, die im Zusammenhang mit FTP-Servern benötigt 
werden.