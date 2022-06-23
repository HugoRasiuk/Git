"""Módulo para mostrar mensajes al usuario
Importe el módulo Msg completo ,
'from Herramientas import Msg' y utilice:
mostrar: para mostrar los mensajes y utilice las sugerencias
al abrir paréntesis para el if de opción seleccionada

Las imágenes de los iconos y de la ventana deben estar con
el prefijo 'Imagenes' dentro del administrador de recursos de QtDesigner"""

import os
import sys
import ctypes
from pickle import load

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QLabel





#Globales
timer_mostrar = QTimer()
timer_cerrar_no = QTimer()
timer_cerrar_si = QTimer()
respuesta = []
VELOCIDAD_OPACIDAD = 0





def mostrar(padre, mensaje, opcion="informar"):
    """Muestra mensajes al usuario

    padre: ventana contenedora,
    mensaje: mensaje a mostrar,
    opcion=informar (informar, preguntar, advertir),
    Pregunta: if "Si" in Msg.respuesta"""
    #Obtenemos  la velocidad de opacidad
    with open("config/config.pic", "rb") as f:
        config = load(f)
    global VELOCIDAD_OPACIDAD
    VELOCIDAD_OPACIDAD = config["velocidad_opacidad"]
    #Obtenemos el tamaño de la pantalla
    user32 = ctypes.windll.user32
    ancho_pantalla = user32.GetSystemMetrics(0)
    alto_pantalla = user32.GetSystemMetrics(1)
    #Configuramos la fuente en función de la pantalla
    tamanio = int(ancho_pantalla * 20 / 1920)
    #Ventana del mensaje
    VentanaMensaje_ = QDialog(parent=padre ,flags=Qt.FramelessWindowHint)
    VentanaMensaje_.setAttribute(Qt.WA_NoSystemBackground, True)
    VentanaMensaje_.setAttribute(Qt.WA_TranslucentBackground, True)
    VentanaMensaje_.setWindowOpacity(0)
    #Central widget de la ventana del mensaje
    VentanaCentral_ = QWidget(VentanaMensaje_)
    valor = int(alto_pantalla * 80 / 1920)
    VentanaCentral_.setStyleSheet(f"""background-color: qlineargradient(
        spread:pad, x1:0, Y1:0, x2:1, y2:0, stop:0.10 rgb(40, 0, 70),
        stop:0.55 rgb(90, 50, 120), stop:1 rgb(190, 100, 220));
        border-radius: {valor}px;
    """)
    #Fuente
    fuente = QtGui.QFont()
    fuente.setPointSize(tamanio)
    #Etiquetas
    lblIcono = QLabel(parent=VentanaCentral_)
    ancho_lblIcono = int(ancho_pantalla * 75 / 1920)
    alto_lblIcono = ancho_lblIcono
    distancia_x = int(ancho_pantalla * 30 / 1920)
    distancia_y = distancia_x
    lblIcono.setGeometry(distancia_x, distancia_y, ancho_lblIcono, alto_lblIcono)
    if opcion == "informar":      
        ruta_imagen = ":/Imagenes/Informar.png"
    elif opcion == "advertir":
        ruta_imagen = ":/Imagenes/Advertir.png"
    else:
        ruta_imagen = ":/Imagenes/Preguntar.png"
    lblIcono.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
    imagen = QImage(ruta_imagen)
    mapa_imagen = QPixmap()
    mapa_imagen.convertFromImage(imagen)
    lblIcono.setScaledContents(True)
    lblIcono.setPixmap(mapa_imagen)
    #
    lblMensaje = QLabel(parent=VentanaCentral_)
    lblMensaje.setWordWrap(True)
    lblMensaje.setAlignment(Qt.AlignCenter)
    lblMensaje.setFont(fuente)
    lblMensaje.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0)")
    lblMensaje.setText(mensaje)
    #Tamaño en pixeles de la cadena
    ancho_pixel_cadena = lblMensaje.fontMetrics().boundingRect(lblMensaje.text()).width()
    alto_pixel_cadena = lblMensaje.fontMetrics().boundingRect(lblMensaje.text()).height()
    distancia_x = int(ancho_pantalla * 60 / 1920 + ancho_lblIcono)
    distancia_y = int(alto_lblIcono * 0.30 + alto_pantalla * 30 / 1080)
    ancho_lblMensaje = int(ancho_pantalla * 550 / 1920)
    alto_renglon = alto_pixel_cadena + alto_pantalla * 10 / 1080
    cantidad_renglones = int(ancho_pixel_cadena / ancho_lblMensaje) + 1
    alto_lblMensaje = alto_renglon * cantidad_renglones
    lblMensaje.setGeometry(distancia_x, distancia_y, ancho_lblMensaje, alto_lblMensaje)
    #Botones
    ancho_boton = int(ancho_pantalla * 60 / 1920)
    alto_boton = ancho_boton
    if opcion == "informar" or opcion == "advertir":
        btnOk = QPushButton(parent=VentanaCentral_)
        btnOk.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        icono_ok = QIcon()
        ruta_imagen_ok = ":/Imagenes/Ok.png"
        icono_ok.addPixmap(QPixmap(ruta_imagen_ok))
        btnOk.setIcon(icono_ok)
        btnOk.setIconSize(QSize(ancho_boton, alto_boton))
        btnOk.clicked.connect(lambda: timer_cerrar_no.start())
    else:
        btnSi = QPushButton(parent=VentanaCentral_)
        btnNo = QPushButton(parent=VentanaCentral_)
        btnSi.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        btnNo.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        icono_si = QIcon()
        icono_no = QIcon()
        ruta_imagen_si = ":/Imagenes/Si.png"
        ruta_imagen_no = ":/Imagenes/No.png"
        icono_si.addPixmap(QPixmap(ruta_imagen_si))
        icono_no.addPixmap(QPixmap(ruta_imagen_no))
        btnSi.setIcon(icono_si)
        btnNo.setIcon(icono_no)
        btnSi.setIconSize(QSize(ancho_boton, alto_boton))
        btnNo.setIconSize(QSize(ancho_boton, alto_boton))
        btnNo.clicked.connect(lambda: timer_cerrar_no.start())
        btnSi.clicked.connect(lambda: timer_cerrar_si.start())
    #definimos tamaño y posición de la ventana
    ancho_ventana = int(ancho_pantalla * 750 / 1920)
    alto_ventana = alto_boton + alto_lblMensaje + alto_pantalla * 120 / 1080
    ventana_x = int((ancho_pantalla - ancho_ventana) / 2)
    ventana_y = int((alto_pantalla - alto_ventana) / 2)
    VentanaMensaje_.setGeometry(ventana_x, ventana_y, ancho_ventana, alto_ventana)
    VentanaCentral_.setGeometry(0, 0, ancho_ventana, alto_ventana)
    #Definimos los botones
    distancia_x = ancho_ventana - ancho_boton - (ancho_pantalla * 30 / 1920)
    distancia_y = alto_ventana - alto_boton - (alto_pantalla * 30 / 1080)
    if opcion == "informar" or opcion == "advertir":
        btnOk.setGeometry(distancia_x, distancia_y, ancho_boton, alto_boton)
    else:
        btnNo.setGeometry(distancia_x, distancia_y, ancho_boton, alto_boton)
        distancia_x = ancho_ventana - ancho_boton * 2 - (ancho_pantalla * 50 / 1920)
        btnSi.setGeometry(distancia_x, distancia_y, ancho_boton, alto_boton)
    #Temporizadores
    timer_mostrar.setInterval(3)
    timer_mostrar.timeout.connect(lambda:  mostrarVentana(VentanaMensaje_))
    #
    timer_cerrar_no.setInterval(3)
    timer_cerrar_no.timeout.connect(lambda: btnOkNoClick(VentanaMensaje_))
    timer_cerrar_si.setInterval(10)
    timer_cerrar_si.timeout.connect(lambda: btnSiclick(VentanaMensaje_))
    #Evento de la tecla escape
    VentanaMensaje_.keyPressEvent = keypressVentanaMensaje
    #Ejecución
    timer_mostrar.start()
    VentanaMensaje_.exec()



def keypressVentanaMensaje(event):
    if event.key() == Qt.Key_Escape:
        timer_cerrar_no.start()


def btnSiclick(contenedor):
    opacidad = contenedor.windowOpacity()
    opacidad -= VELOCIDAD_OPACIDAD
    contenedor.setWindowOpacity(opacidad)
    if contenedor.windowOpacity() <= 0:
        global respuesta
        respuesta.clear()
        respuesta.append("Si")
        timer_cerrar_si.stop()
        contenedor.close()



def btnOkNoClick(contenedor):
    opacidad = contenedor.windowOpacity()
    opacidad -= VELOCIDAD_OPACIDAD
    contenedor.setWindowOpacity(opacidad)
    if contenedor.windowOpacity() <= 0: 
        global respuesta
        respuesta.clear()
        respuesta.append("No")
        timer_cerrar_no.stop()
        contenedor.close()
        


def mostrarVentana(contenedor):
    opacidad = contenedor.windowOpacity()
    global VELOCIDAD_OPACIDAD
    opacidad += VELOCIDAD_OPACIDAD
    contenedor.setWindowOpacity(opacidad)
    if contenedor.windowOpacity() >= 1:
        timer_mostrar.stop()
