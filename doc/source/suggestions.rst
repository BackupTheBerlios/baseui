Wunschliste
===========
Die Historie muss komplett überarbeitet werden. Keine schlechte Idee, dies im
Modul SQLdb.py direkt zu tun. Was ist eigentlich Historie? Man müsste eigentlich
immer nur den Stand vor dem aktuellen Update, Delete oder Insert sichern. Bei
Update und Delete ganz einfach, Insert hat halt einfach keinen Altstand.

Gegenwärtig ist old_content und new_content im rumgeistern. Das gilt es 
abzustellen, weil es einfach nicht notwendig ist, den neuen Stand doppelt
zu sichern. Es funktioniert aber erstmal!