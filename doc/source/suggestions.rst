Wunschliste
===========
Die Historie muss komplett �berarbeitet werden. Keine schlechte Idee, dies im
Modul SQLdb.py direkt zu tun. Was ist eigentlich Historie? Man m�sste eigentlich
immer nur den Stand vor dem aktuellen Update, Delete oder Insert sichern. Bei
Update und Delete ganz einfach, Insert hat halt einfach keinen Altstand.

Gegenw�rtig ist old_content und new_content im rumgeistern. Das gilt es 
abzustellen, weil es einfach nicht notwendig ist, den neuen Stand doppelt
zu sichern. Es funktioniert aber erstmal!