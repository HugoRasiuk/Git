"""Módulo para el acceso al sistema"""

"""
Hola Lala!!! gracias por compartir todos estos proyectos con migo, soy muy felpiz 
con vos. TE AMOOO MUCHOOO!!!
Que mejor lugar que este para decirte lo que siento dado que Python nos
unió desde el principio, jajaja
te mando muchos besitos y millones de cerebritos haciendo sinapsis entre ellos con
millones ded rayitos multicolores. Gracias de verdad!!!, sos un ser genial!!!

Acá te voy anotando los botones.
btnIngresar
btnSalir
btnRecuperarPorPregunta
btnRecuperarPorContrasenia
btnAceptarContrasenia
btnCancelarContrasenia
btnAceptarPregunta
btnCancelarPregunta

Acá los txt
txtUsuario
txtContrasenia
txtContraseniaAnterior
txtRespuesta
"""

import ctypes
from pickle import load

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer

from Interfaces.guiAcceso import Ui_frmAcceso


class VentanaAcceso(QMainWindow, Ui_frmAcceso):
    def __init__(self, padre):
        QMainWindow.__init__(self, parent=padre)
        self.setupUi(self)
        # quitamos bordes y transparentamos esquinas
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #Obtenemos el ancho y alto de la pantalla
        user32 = ctypes.windll.user32
        self.ancho_pantalla = user32.GetSystemMetrics(0)
        self.alto_pantalla = user32.GetSystemMetrics(1)
        #Limpiamos el pie de la ventana.
        self.line.close()
        self.limpiarPieVentanaIngresar()
        #Cargamos el combo de preguntas
        self.cargarCombo()
        #Centramos la ventana
        self.ancho_ventana = self.width()
        self.alto_ventana = self.height()
        x = int((self.ancho_pantalla - self.ancho_ventana) / 2)
        y = int((self.alto_pantalla - self.alto_ventana) / 2)
        self.setGeometry(x, y, self.ancho_ventana, self.alto_ventana)
        #eventos click.
        self.btnSalir.clicked.connect(self.clickBtnSalir)
        self.btnOlvideContrasenia.clicked.connect(self.clickOlvideContrasenia)
        self.btnRecuperarPorContrasenia.clicked.connect(self.clickBtnRecuperarPorContrasenia)
        self.btnRecuperarPorPregunta.clicked.connect(self.clickBtnRecuperarPorPregunta)
        self.btnAceptarContrasenia.clicked.connect(self.clickBtnAceptarContrasenia)
        self.btnCancelarContrasenia.clicked.connect(self.clickBtnCancelarContrasenia)
        self.btnAceptarPregunta.clicked.connect(self.clickBtnAceptarPregunta)
        self.btnCancelarPregunta.clicked.connect(self.clickBtnCancelarPregunta)





    #Métodos generales
    def ingresar(self, tmrPrincipal, vel_expansion):
        """Se ejecuta desde la ventana principal"""
        self.tmrPrincipal = tmrPrincipal
        self.VELOCIDAD_EXPANSION = vel_expansion
        self.show()

    def limpiarPieVentanaIngresar(self):
        """Limpia la parte inferior de la ventana de acceso"""
        self.btnRecuperarPorContrasenia.close()
        self.btnRecuperarPorPregunta.close()
        self.lblContraseniaAnterior.close()
        self.txtContraseniaAnterior.close()
        self.btnAceptarContrasenia.close()
        self.btnCancelarContrasenia.close()
        self.cbxPreguntas.close()
        self.txtRespuesta.close()
        self.btnAceptarPregunta.close()
        self.btnCancelarPregunta.close()

    def mostrarBotones(self):
        """Muesgtra los botones de opción de ingreso por
        olvido de contraseña"""
        self.line.show()
        self.btnRecuperarPorContrasenia.show()
        self.btnRecuperarPorPregunta.show()

    def mostrarContraseniaAnterior(self):
        """Muestra lo necesario para el ingreso por contraseña anterior."""
        self.lblContraseniaAnterior.show()
        self.txtContraseniaAnterior.show()
        self.btnAceptarContrasenia.show()
        self.btnCancelarContrasenia.show()
        self.txtContraseniaAnterior.setFocus()

    def mostrarPreguntas(self):
        self.cbxPreguntas.show()
        self.txtRespuesta.show()
        self.btnAceptarPregunta.show()
        self.btnCancelarPregunta.show()
        self.cbxPreguntas.setFocus()

    def cargarCombo(self):
        self.cbxPreguntas.addItem("Cantante o grupo de música favorito")
        self.cbxPreguntas.addItem("Comida favorita")
        self.cbxPreguntas.addItem("Número favorito")
        self.cbxPreguntas.addItem("Animal favorito")
        self.cbxPreguntas.addItem("Película favorita")
        self.cbxPreguntas.addItem("Libro favorito")
        self.cbxPreguntas.addItem("Lugar de nacimiento")
        self.cbxPreguntas.addItem("Escuela donde estudió")
        self.cbxPreguntas.addItem("Nombre de la mascota")
        self.cbxPreguntas.setCurrentIndex(0)





    #Eventos click.
    def clickBtnSalir(self):
        self.tmrPrincipal.start()

    def clickOlvideContrasenia(self):
        tope = 0
        while tope < int(self.alto_pantalla * 100 / 1080):
            tope += self.VELOCIDAD_EXPANSION
            self.setGeometry(self.x(), self.y(), self.ancho_ventana,
                             self.alto_ventana + tope)
        self.line.show()
        self.btnRecuperarPorContrasenia.show()
        self.btnRecuperarPorPregunta.show()

    def clickBtnRecuperarPorContrasenia(self):
        self.limpiarPieVentanaIngresar()
        self.mostrarContraseniaAnterior()

    def clickBtnRecuperarPorPregunta(self):
        self.limpiarPieVentanaIngresar()
        self.mostrarPreguntas()

    def clickBtnAceptarContrasenia(self):
        pass

    def clickBtnCancelarContrasenia(self):
        self.limpiarPieVentanaIngresar()
        self.mostrarBotones()

    def clickBtnAceptarPregunta(self):
        pass

    def clickBtnCancelarPregunta(self):
        self.limpiarPieVentanaIngresar()
        self.mostrarBotones()
