:mod:`Containers` --- Container widgets
=======================================

.. module:: Containers
   :synopsis: Container widgets
   
Ein Modul zum händeln von Container widgets.



.. class:: Window(widget=None)

   Diese Klasse vereinfacht immer wieder kehrende Funktionen, die auf Fenster 
   angewandt werden.
   

.. method:: Window.remove_focus()

   Stellt fest, ob das Fenster modal ist und setzt es auf nicht modal. 
   Gleichzeitig wird in der Variable ``self.modal`` gemerkt, ob das Fenster 
   vorher modal war. Diese Funktion wird intern von GTKapi angewandt, um 
   Dialogboxen und überlagernde Fenster in der Vordergrund zu bringen.
   
   
.. method:: Window.restore_focus()

   Wenn das Fenster vor Anwendung der Methode remove_focus modal war, wird es 
   wieder modal gemacht. Diese Funktion wird intern von GTKapi angewandt, um 
   Dialogboxen und überlagernde Fenster in der Vordergrund zu bringen.
   

