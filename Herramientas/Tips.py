"""Módulo para mosgtrar tooltips"""

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QCursor

import ctypes





#Globales
lblTip = None
tmrEncender = QTimer()
tmrApagar = QTimer()





def mostrar(texto, contenedor, widget):
    """Muestra tooltips

    texto: texto a mostrar,
    contenedor: ventana padre,
    widget: widget al que hace referencia el tooltip."""
    #Evento al salir del widget
    widget.leaveEvent = quitarLabel
    #Obgenemos el ancho de la pantalla
    user32 = ctypes.windll.user32
    ancho_pantalla = user32.GetSystemMetrics(0)
    alto_pantalla = user32.GetSystemMetrics(1)
    #Tamaño de la ventana contenedora
    contenedor_x = contenedor.x()
    contenedor_y = contenedor.y()
    #Instanciamos el label
    global lblTip
    lblTip = QLabel(texto, contenedor)
    #tamaño de fuente
    tamanio = ancho_pantalla * 15 / 1920
    fuente = QtGui.QFont()
    fuente.setPointSize(tamanio)
    lblTip.setFont(fuente)
    #Ancho del label del tooltip
    ancho_lbl = lblTip.fontMetrics().boundingRect(lblTip.text()).width() + (ancho_pantalla * 20 / 1920)
    alto_lbl = lblTip.fontMetrics().boundingRect(lblTip.text()).height() + (alto_pantalla * 10 / 1080)
    #Determinamos si el tooltip va a la izquierda o derecha
    if (widget.x() + ancho_lbl + widget.width()) > contenedor.width():
        pos_x = widget.x() - ancho_lbl
    else:
        pos_x = widget.x() + widget.width()
    pos_y = widget.y()
    #Ubicación y tamaño del tooltip
    lblTip.setGeometry(pos_x, pos_y, ancho_lbl, alto_lbl)
    #características del tooltip
    valor = int(ancho_pantalla * 10 / 1920)
    lblTip.setStyleSheet(f"background-color: rgb(255, 255, 150); color: black; border-radius: {valor}px")
    lblTip.setAlignment(Qt.AlignCenter)
    #características de los timers
    global tmrEncender
    tmrEncender.timeout.connect(lambda: lblTip.show())
    tmrEncender.setSingleShot(True)
    tmrEncender.start(2000)
    global tmrApagar
    tmrApagar.timeout.connect(quitarLabelTiempo)
    tmrApagar.setSingleShot(True)
    tmrApagar.start(5000)

def quitarLabelTiempo():
    """Quita el Tooltip de pantalla por tiempo transcurrido"""
    global lblTip
    lblTip.close()

def quitarLabel(Event):
    """Quita el Tooltip de pantalla por salida del mouse del widget"""
    global tmrApagar
    global tmrEncender
    global lblTip
    lblTip.close()
    tmrEncender.stop()
    tmrApagar.stop()
