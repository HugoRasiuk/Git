"""Botones del módulo:
btnGuardar
btnBorrar
btnCerrar

Acá los nombres de los txt:
txtNombre
txtApellido
txtUsuario
txtContraseniaActual
txtContraseniaNueva
txtContraseniaRepetir

Acá los check box:
chkMusica
chkComida
chkNumero
chkAnimal
chkLibro
chkLugarNacimiento
chkEscuela
chkMascota

Los txt asociados a los check box:
txtMusica
txtComida
txtNumero
txtAnimal
txtLibro
txtLugarNacimiento
txtEscuela
txtMascota
"""



"""Módulo para el cambio de contraseña de usuario y administrador"""

import ctypes

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer

from Interfaces.guiCambioContrasenia import Ui_frmCambioContrasenia





class VentanaCambioContrasenia(QMainWindow, Ui_frmCambioContrasenia):
    def __init__(self, padre):
        QMainWindow.__init__(self, parent=padre)
        self.setupUi(self)
        # quitamos bordes y transparentamos esquinas
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #Obtenemos el ancho y alto de la pantalla
        user32 = ctypes.windll.user32
        ancho_pantalla = user32.GetSystemMetrics(0)
        alto_pantalla = user32.GetSystemMetrics(1)
        #Centramos la ventana
        ancho_ventana = self.width()
        alto_ventana = self.height()
        x = int((ancho_pantalla - ancho_ventana) / 2)
        y = alto_pantalla * 290 / 1080
        self.setGeometry(x, y, ancho_ventana, alto_ventana)
        #Timers
        self.tmrSoftIn = QTimer()
        self.tmrSoftIn.setInterval(5)
        #self.tmrSoftIn.timeout.connect(self.softIn)
        #
        self.tmrSoftOut = QTimer()
        self.tmrSoftOut.setInterval(5)
        #self.tmrSoftOut.timeout.connect(self.softOut)
        #Eventos click
        self.btnCerrar.clicked.connect(lambda: self.close())