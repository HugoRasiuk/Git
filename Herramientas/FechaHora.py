"""Módulo para mostrar la fecha y hora"""""""""
from PyQt5.QtCore import QDateTime



def mostrarFechaHora(widget_fecha=None, widget_hora=None):
    """Muestra la fecha y la hora

    widget_fecha label donde se mostrará la fecha.
    widget_hora LCD number donde se mostrará la hora."""
    if widget_hora != None:
        widget_hora.display(QDateTime.currentDateTime().toString("hh:mm:ss"))
    if widget_fecha != None:
        widget_fecha.adjustSize()
        widget_fecha.setText("Hoy es " + QDateTime.currentDateTime().toString("dddd dd")
        + " de " + QDateTime.currentDateTime().toString("MMMM")
        + " de " + QDateTime.currentDateTime().toString("yyyy"))