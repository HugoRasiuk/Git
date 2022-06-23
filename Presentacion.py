"""Módulo de la presentación de la empresa"""

import ctypes
from pickle import load

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont





class VentanaPresentacion(QMainWindow):
    def __init__(self):
        super().__init__()
        #Obtenemos el tamaño de la pantalla
        user32 = ctypes.windll.user32
        self.ancho_pantalla = user32.GetSystemMetrics(0)
        self.alto_pantalla = user32.GetSystemMetrics(1)
        #Quitamos bordes y transparentamos la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0)
        #Central widget de la presentación
        self.ventana_central_ = QWidget(self)
        self.ventana_central_.setGeometry(
            0, 0, self.ancho_pantalla * 700 / 1920, self.alto_pantalla * 700 / 1080)
        #Características de la interfaz
        #Definimos tamaño y posicion de la ventana
        self.ancho_ventana =int(self.ancho_pantalla * 700 / 1920)
        self.alto_ventana = int(self.alto_pantalla * 700 / 1080)
        self.ventana_x = int((self.ancho_pantalla - self.ancho_ventana) / 2)
        self.ventana_y = int((self.alto_pantalla - self.alto_ventana) / 2)
        self.setGeometry(self.ventana_x, self.ventana_y, self.ancho_pantalla * 700 / 1920, self.alto_pantalla * 700 / 1080)
        self.radio = int(self.ancho_ventana / 2)
        self.setStyleSheet(f"background-color: white; border-radius: {self.radio}px")
        #Timers
        self.tmrSoftIn = QTimer()
        self.tmrSoftIn.setInterval(0)
        self.tmrSoftIn.timeout.connect(self.softIn)
        #
        self.tmrSoftOut = QTimer()
        self.tmrSoftOut.setInterval(15)
        self.tmrSoftOut.timeout.connect(self.softOut)
        #Obtenemos la velocidad de la OPACIDAD.
        self.obtenerVelocidadAnimacion()

    def obtenerVelocidadAnimacion(self):
        """Obtiene valores de configuración desde un archivo pickle."""
        with open("config/config.pic", "rb") as f:
            config = load(f)
        self.VELOCIDAD_OPACIDAD = config["velocidad_opacidad"]

    def softIn(self):
        """Muestra suavemente la ventana"""
        opacidad = self.windowOpacity()
        opacidad += self.VELOCIDAD_OPACIDAD
        self.setWindowOpacity(opacidad)
        if self.windowOpacity() >= 1:
            self.tmrSoftIn.stop()
            self.mostrarLogo()
            self.tmrSoftOut.start()

    def mostrarLogo(self):
        self.logo_ = VentanaPresentacionLogo()
        self.logo_.show()
        self.raise_()
        self.logo_.setWindowOpacity(1)

    def softOut(self):
        """Desaparece suavemente la ventana"""
        opacidad = self.windowOpacity()
        opacidad -= self.VELOCIDAD_OPACIDAD
        self.setWindowOpacity(opacidad)
        if self.windowOpacity() <= 0:
            self.tmrSoftOut.stop()
            self.logo_.tmrRetardo.start(100)
            self.logo_.tmrSoftOut.start()
            self.close()

            



class VentanaPresentacionLogo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.indice = 0
        #Obtenemos el tamaño de la pantalla
        user32 = ctypes.windll.user32
        self.ancho_pantalla = user32.GetSystemMetrics(0)
        self.alto_pantalla = user32.GetSystemMetrics(1)
        #Quitamos bordes y transparentamos la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0)
        #Central widget de la presentación
        self.ventana_central_ = QWidget(self)
        self.ventana_central_.setGeometry(
            0, 0, self.ancho_pantalla * 700 / 1920, self.alto_pantalla * 700 / 1080)
        #Botón con el logo
        self.btnLogo = QPushButton(parent=self)
        self.btnLogo.setText("LH")
        self.font = QFont()
        self.font.setFamily("Lobster")
        self.font.setPointSize(int(self.ancho_pantalla * 300 / 1920))
        self.btnLogo.setFont(self.font)
        self.btnLogo.setStyleSheet(
            "background-color: rgba(150, 0, 0, 1); color: rgb(170, 170, 170)")
        self.btnLogo.setGeometry(
            self.ancho_pantalla * 120 / 1920, self.alto_pantalla * 70 / 1080, self.ancho_pantalla * 400 / 1920, self.alto_pantalla * 400 / 1080)
        #Fuente para la palabra software
        self.font_lbl = QFont()
        self.font_lbl.setFamily("Times New Roman")
        self.font_lbl.setPointSize(int(self.ancho_pantalla * 300 / 1920))
        #Letras de la palabra Software
        self.letras = [letra for letra in "Software"]
        #Creamos los labels
        self.labels = []
        self.lbl_1 = QLabel(parent=self)
        self.lbl_2 = QLabel(parent=self)
        self.lbl_3 = QLabel(parent=self)
        self.lbl_4 = QLabel(parent=self)
        self.lbl_5 = QLabel(parent=self)
        self.lbl_6 = QLabel(parent=self)
        self.lbl_7 = QLabel(parent=self)
        self.lbl_8 = QLabel(parent=self)
        self.labels.append(self.lbl_1)
        self.labels.append(self.lbl_2)
        self.labels.append(self.lbl_3)
        self.labels.append(self.lbl_4)
        self.labels.append(self.lbl_5)
        self.labels.append(self.lbl_6)
        self.labels.append(self.lbl_7)
        self.labels.append(self.lbl_8)
        indice = 0
        for elemento in self.labels:
            elemento.setText(self.letras[indice])
            elemento.setFont(self.font_lbl)
            elemento.setGeometry(
                int(self.ancho_pantalla * 200 / 1920),
                int(self.alto_pantalla * 100 / 1080),
                int(self.ancho_pantalla * 410 / 1920),
                int(self.alto_pantalla * 520 / 1080)
            )
            elemento.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0)")
            elemento.setVisible(False)
            indice += 1
        #Características de la interfaz
        #Definimos tamaño y posicion de la ventana
        self.ancho_ventana = int(self.ancho_pantalla * 700 / 1920)
        self.alto_ventana = int(self.alto_pantalla * 700 / 1080)
        self.ventana_x = int((self.ancho_pantalla - self.ancho_ventana) / 2)
        self.ventana_y = int((self.alto_pantalla - self.alto_ventana) / 2)
        self.setGeometry(self.ventana_x, self.ventana_y,
            self.ancho_pantalla * 700 / 1920, self.alto_pantalla * 700 / 1080)
        self.radio = int(self.ancho_ventana / 2)
        self.setStyleSheet(
            f"""background-color: rgb(150, 0, 0);
            border-radius: {self.radio}px""")
        #Timers
        self.tmrSoftOut = QTimer()
        self.tmrSoftOut.setInterval(15)
        self.tmrSoftOut.timeout.connect(self.softOut)
        #
        self.tmrRetardo = QTimer()
        self.tmrRetardo.setSingleShot(True)
        self.tmrRetardo.timeout.connect(lambda: self.tmrMostrarLetras.start())
        #
        self.tmrMostrarLetras = QTimer()
        self.tmrMostrarLetras.setInterval(0)
        self.tmrMostrarLetras.timeout.connect(self.mostrarLetras)
        #
        self.tmrReducirFuente = QTimer()
        self.tmrReducirFuente.setInterval(0)
        self.tmrReducirFuente.timeout.connect(self.reducirFuente)
        #
        self.tmrMostrarLogo = QTimer()
        self.tmrMostrarLogo.setSingleShot(True)
        self.tmrMostrarLogo.timeout.connect(self.mostrar)
        #Obtenemos la velocidad de la OPACIDAD.
        self.obtenerVelocidadAnimacion()

    def obtenerVelocidadAnimacion(self):
        """Obtiene valores de configuración desde un archivo pickle."""
        with open("config/config.pic", "rb") as f:
            config = load(f)
        self.VELOCIDAD_OPACIDAD = config["velocidad_opacidad"]

    def softOut(self):
        """Desaparece suavemente la ventana"""
        opacidad = self.windowOpacity()
        if not self.tmrRetardo.isActive() and not self.tmrMostrarLetras.isActive() and not self.tmrReducirFuente.isActive() and not self.tmrMostrarLogo.isActive():
            opacidad -= self.VELOCIDAD_OPACIDAD
        self.setWindowOpacity(opacidad)
        if self.windowOpacity() <= 0:
            self.tmrSoftOut.stop()
            self.close()

    def mostrarLetras(self):
        self.tamanio_fuente = 500
        if self.indice < 8:
            self.pos_x = int(self.ancho_pantalla * 200 / 1920)
            self.pos_y = int(self.alto_pantalla * 100 / 1080)
            self.labels[self.indice].setVisible(True)
            self.tmrReducirFuente.start()
            self.tmrMostrarLetras.stop()
        else:
            #Timer para el tiempo visible del logo terminado
            self.tmrMostrarLogo.start(500)
            self.tmrMostrarLetras.stop()

    def reducirFuente(self):
        self.font_lbl.setPointSize(
            int(self.ancho_pantalla * self.tamanio_fuente / 1920))
        self.labels[self.indice].setFont(self.font_lbl)
        self.tamanio_fuente -= 2
        if self.indice == 0:
            self.pos_x -= 0.1
        if self.indice == 1:
            self.pos_x += 0.1
        if self.indice == 2:
            self.pos_x += 0.3
        if self.indice == 3:
            self.pos_x += 0.5
        if self.indice == 4:
            self.pos_x += 0.7
        if self.indice == 5:
            self.pos_x += 0.9
        if self.indice == 6:
            self.pos_x += 1.1
        if self.indice == 7:
            self.pos_x += 1.3
        self.pos_y += 0.8
        self.labels[self.indice].setGeometry(
            int(self.ancho_pantalla * self.pos_x / 1920),
            int(self.alto_pantalla * self.pos_y / 1080),
            int(self.ancho_pantalla * 410 / 1920),
            int(self.alto_pantalla * 520 / 1080)
        )
        if self.tamanio_fuente == 40:
            self.indice += 1
            self.tmrMostrarLetras.start()
            self.tmrReducirFuente.stop()

    def mostrar(self):
        pass
