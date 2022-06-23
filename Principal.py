"""Módulo principal del proyecto de odontología"""

import sys
import ctypes
from time import time
from pickle import load, dump

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

from Herramientas.FechaHora import mostrarFechaHora
from Herramientas import Msg

from Interfaces.guiPrincipal import Ui_frmPrincipal
from Presentacion import VentanaPresentacion
from CambioContrasenia import VentanaCambioContrasenia
from Acceso import VentanaAcceso





class ventanaPrincipal(QMainWindow, Ui_frmPrincipal):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # quitamos bordes
        self.setWindowFlags(Qt.FramelessWindowHint)
        #Obtenemos el ancho y alto de la pantalla
        user32 = ctypes.windll.user32
        self.ancho_pantalla = user32.GetSystemMetrics(0)
        self.alto_pantalla = user32.GetSystemMetrics(1)
        #Variables de control
        self.btn_pacientes_click = False
        self.btn_informes_click = False
        #Características de la interfaz
        self.setGeometry(0, 0, int(self.ancho_pantalla * 1920 / 1920), int(
            self.alto_pantalla * 1080 / 1080))
        self.setWindowOpacity(0)
        # Ocultamos los botones de los submenus
        # Pacientes
        self.btnAtencionPacientes.close()
        self.btnGestionPacientes.close()
        # Informes
        self.btnInformesPagos.close()
        self.btnInformesCobros.close()        
        #Instancias de interfaz
        self.ventana_cambio_contrasenia_ = VentanaCambioContrasenia(self)
        self.ventana_acceso_ = VentanaAcceso(self)
        #timers
        self.tmrFechaHora = QTimer()
        self.tmrFechaHora.setInterval(1000)
        self.tmrFechaHora.timeout.connect(lambda: mostrarFechaHora(
            self.lblFecha, self.lcdHora))
        #
        self.tmrSoftIn = QTimer()
        self.tmrSoftIn.setInterval(10)
        self.tmrSoftIn.timeout.connect(self.softIn)
        #
        self.tmrSoftOut = QTimer()
        self.tmrSoftOut.setInterval(10)
        self.tmrSoftOut.timeout.connect(self.softOut)
        #
        self.tmrExpandirUsuarios = QTimer()
        self.tmrExpandirUsuarios.setInterval(1)
        self.tmrExpandirUsuarios.timeout.connect(self.expandirBtnUsuarios)
        #
        self.tmrContraerUsuarios = QTimer()
        self.tmrContraerUsuarios.setInterval(1)
        self.tmrContraerUsuarios.timeout.connect(self.contraerBtnUsuarios)
        #
        self.tmrExpandirSalir = QTimer()
        self.tmrExpandirSalir.setInterval(1)
        self.tmrExpandirSalir.timeout.connect(self.expandirBtnSalir)
        #
        self.tmrContraerSalir = QTimer()
        self.tmrContraerSalir.setInterval(1)
        self.tmrContraerSalir.timeout.connect(self.contraerBtnSalir)
        #
        self.tmrExpandirPacientes = QTimer()
        self.tmrExpandirPacientes.setInterval(1)
        self.tmrExpandirPacientes.timeout.connect(self.expandirBtnPacientes)
        #
        self.tmrContraerPacientes = QTimer()
        self.tmrContraerPacientes.setInterval(1)
        self.tmrContraerPacientes.timeout.connect(self.contraerBtnPacientes)
        #
        self.tmrExpandirInformes = QTimer()
        self.tmrExpandirInformes.setInterval(1)
        self.tmrExpandirInformes.timeout.connect(self.expandirBtnInformes)
        #
        self.tmrContraerInformes = QTimer()
        self.tmrContraerInformes.setInterval(1)
        self.tmrContraerInformes.timeout.connect(self.contraerBtnInformes)
        #
        self.tmrExpandirNotas = QTimer()
        self.tmrExpandirNotas.setInterval(1)
        self.tmrExpandirNotas.timeout.connect(self.expandirBtnNotas)
        #
        self.tmrContraerNotas = QTimer()
        self.tmrContraerNotas.setInterval(1)
        self.tmrContraerNotas.timeout.connect(self.contraerBtnNotas)
        #
        self.tmrExpandirNosotros = QTimer()
        self.tmrExpandirNosotros.setInterval(1)
        self.tmrExpandirNosotros.timeout.connect(self.expandirBtnNosotros)
        #
        self.tmrContraerNosotros = QTimer()
        self.tmrContraerNosotros.setInterval(1)
        self.tmrContraerNosotros.timeout.connect(self.contraerBtnNosotros)
        #
        self.tmrDesplegar = QTimer()
        self.tmrDesplegar.setInterval(1)
        self.tmrDesplegar.timeout.connect(self.mostrarBotones)
        #Eventos del teclado
        self.keyPressEvent = self.teclaPresionadaEvent
        #Eventos del mouse
        self.btnUsuarios.enterEvent = self.enterBtnUsuarios
        self.btnUsuarios.leaveEvent = self.leaveBtnUsuarios
        self.btnSalir.enterEvent = self.enterBtnSalir
        self.btnSalir.leaveEvent = self.leaveBtnSalir
        self.btnPacientes.enterEvent = self.enterBtnPacientes
        self.btnPacientes.leaveEvent = self.leaveBtnPacientes
        self.btnInformes.enterEvent = self.enterBtnInformes
        self.btnInformes.leaveEvent = self.leaveBtnInformes
        self.btnNotas.enterEvent = self.enterBtnNotas
        self.btnNotas.leaveEvent = self.leaveBtnNotas
        self.btnNosotros.enterEvent = self.enterBtnNosotros
        self.btnNosotros.leaveEvent = self.leaveBtnNosotros
        #Eventos click
        self.btnCerrar.clicked.connect(self.clickBtnSalir)
        self.btnSalir.clicked.connect(self.clickBtnSalir)
        self.btnMinimizar.clicked.connect(lambda: self.showMinimized())
        self.btnPacientes.clicked.connect(self.clickBtnPacientes)
        self.btnInformes.clicked.connect(self.clickBtnInformes)
        #Cargamos las constantes con las velocidades
        self.cargarConfig()





    def cargarConfig(self):
        """Obtiene valores de configuración desde un archivo pickle."""
        with open("config/config.pic", "rb") as f:
            config = load(f)
        if "velocidad_opacidad" in config:
            self.VELOCIDAD_OPACIDAD = config["velocidad_opacidad"]
        else:
            self.calcularVelocidadOpacidad()
            config["velocidad_opacidad"] = self.VELOCIDAD_OPACIDAD
            with open("config/config.pic", "wb") as f:
                dump(config, f)
        if "velocidad_expansion" in config:
            self.VELOCIDAD_EXPANSION = config["velocidad_expansion"]
        else:
            self.calcularVelocidadExpansion()
            config["velocidad_expansion"] = self.VELOCIDAD_EXPANSION
            with open("config/config.pic", "wb") as f:
                dump(config, f)
        if "velocidad_animacion" in config:
            self.VELOCIDAD_ANIMACION = config["velocidad_animacion"]
        else:
            self.calcularVelocidadAnimacion()
            config["velocidad_animacion"] = self.VELOCIDAD_ANIMACION
            with open("config/config.pic", "wb") as f:
                dump(config, f)

    def calcularVelocidadAnimacion(self):
        """calcula los valores de velocidad de las animaciones."""
        lista = []
        diferencia = 0
        tiempo_actual = time()
        while diferencia < 0.5:
            diferencia = time() - tiempo_actual
            lista.append("Lala y Hugo")
        self.VELOCIDAD_ANIMACION = int(1500000 * 20 / len(lista))
        del(lista)

    def calcularVelocidadExpansion(self):
        """calcula el valor de la expansión."""
        lista = []
        diferencia = 0
        tiempo_actual = time()
        while diferencia < 0.5:
            diferencia = time() - tiempo_actual
            lista.append("Lala y Hugo")
        self.VELOCIDAD_EXPANSION = int(750000 * 2 / len(lista))
        del(lista)

    def calcularVelocidadOpacidad(self):
        """calcula el valor de la velocidad de la opacidad."""
        lista = []
        diferencia = 0
        tiempo_actual = time()
        while diferencia < 0.5:
            diferencia = time() - tiempo_actual
            lista.append("Lala y Hugo")
        self.VELOCIDAD_OPACIDAD = round(750000 * 0.02 / len(lista), 2)
        if self.VELOCIDAD_OPACIDAD < 0.01:
            self.VELOCIDAD_OPACIDAD = 0.01
        del(lista)


    #Eventos click
    def clickBtnPacientes(self):
        #Variable para saber que se hizo click en el botón
        self.btn_pacientes_click = True
        #Obtenemos los valores para los botones del menu desplegable
        self.x = self.btnPacientesDesplegable.x()
        self.y = self.btnPacientesDesplegable.y()
        self.ancho = int(self.ancho_pantalla * 200 / 1920)
        self.alto = int(self.alto_pantalla * 40 / 1080)
        self.x += int(self.ancho_pantalla * 80 / 1920)
        self.y += int(self.alto_pantalla * 10 / 1080)
        self.tpl = (self.btnAtencionPacientes, self.btnGestionPacientes)        
        #Mostramos todos los botones detrás del botón desplegado
        for boton in self.tpl:
            boton.setGeometry(self.x, self.y, self.ancho, self.alto)
            boton.show()
        #Cantidad de desplazamiento de los botones
        self.avance = 0
        #Indice para el control  del despliegue de botones
        self.indice = 0
        self.tmrDesplegar.start()

    def clickBtnInformes(self):
        # Variable para saber que se hizo click en el botón
        self.btn_informes_click = True
        #Obtenemos los valores para los botones del menu desplegable
        self.x = self.btnInformesDesplegable.x()
        self.y = self.btnInformesDesplegable.y()
        self.ancho = int(self.ancho_pantalla * 200 / 1920)
        self.alto = int(self.alto_pantalla * 40 / 1080)
        self.x += int(self.ancho_pantalla * 80 / 1920)
        self.y += int(self.alto_pantalla * 10 / 1080)
        self.tpl = (self.btnInformesPagos, self.btnInformesCobros)
        #Mostramos todos los botones detrás del botón desplegado
        for boton in self.tpl:
            boton.setGeometry(self.x, self.y, self.ancho, self.alto)
            boton.show()
        #Cantidad de desplazamiento de los botones
        self.avance = 0
        #Indice para el control  del despliegue de botones
        self.indice = 0
        self.tmrDesplegar.start()

    def clickBtnSalir(self):
        Msg.mostrar(self, "¿Desea salir del programa?", "preguntar")
        if "Si" in Msg.respuesta:
            self.tmrSoftOut.start()




    #Eventos enter y leave
    def enterBtnNosotros(self, event):
        """Acciones al entrar el mouse en el botón nosotros"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerNosotros.stop()
        self.tmrExpandirNosotros.start()

    def leaveBtnNosotros(self, event):
        """Acciones al salir el mouse del botón nosotros"""
        self.tmrExpandirNosotros.stop()
        self.tmrContraerNosotros.start()

    def enterBtnNotas(self, event):
        """Acciones al entrar el mouse en el botón notas"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerNotas.stop()
        self.tmrExpandirNotas.start()

    def leaveBtnNotas(self, event):
        """Acciones al salir el mouse del botón notas"""
        self.tmrExpandirNotas.stop()
        self.tmrContraerNotas.start()

    def enterBtnInformes(self, event):
        """Acciones al entrar el mouse en el botón informes"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerInformes.stop()
        self.tmrExpandirInformes.start()

    def leaveBtnInformes(self, event):
        """Acciones al salir el mouse del botón informes"""
        if not self.btn_informes_click:
            self.tmrExpandirInformes.stop()
            self.tmrContraerInformes.start()
        else:
            self.btn_informes_click = False

    def enterBtnPacientes(self, event):
        """Acciones al entrar el mouse en el botón pacientes"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerPacientes.stop()
        self.tmrExpandirPacientes.start()

    def leaveBtnPacientes(self, event):
        """Acciones al salir el mouse del botón pacientes"""
        if not self.btn_pacientes_click:
           self.tmrExpandirPacientes.stop()
           self.tmrContraerPacientes.start()
        else:
           self.btn_pacientes_click = False

    def enterBtnSalir(self, event):
        """Acciones al entrar el mouse en el botón salir"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerSalir.stop()
        self.tmrExpandirSalir.start()

    def leaveBtnSalir(self, event):
        """Acciones al salir el mouse del botón salir"""
        self.tmrExpandirSalir.stop()
        self.tmrContraerSalir.start()

    def enterBtnUsuarios(self, event):
        """Acciones al entrar el mouse en el botón Usuarios"""
        self.quitarBotones()
        self.contraerBotones()
        self.tmrContraerUsuarios.stop()
        self.tmrExpandirUsuarios.start()

    def leaveBtnUsuarios(self, event):
        """Acciones al salir el mouse del botón Usuarios"""
        self.tmrExpandirUsuarios.stop()
        self.tmrContraerUsuarios.start()




    #Métodos generales
    def mostrarBotones(self):
        """Despliega el menu de botones"""
        self.avance += self.VELOCIDAD_EXPANSION
        self.y += self.VELOCIDAD_EXPANSION
        for boton in self.tpl[self.indice:]:
            boton.setGeometry(self.x, self.y, self.ancho, self.alto)
        if self.avance == 40:
            self.avance = 0
            self.indice += 1
            if self.indice == len(self.tpl):
                self.tmrDesplegar.stop()

    def quitarBotones(self):
        """Quita los botones de los menu desplegables"""
        self.btnAtencionPacientes.close()
        self.btnGestionPacientes.close()
        self.btnInformesPagos.close()
        self.btnInformesCobros.close()
    
    def contraerBotones(self):
        """Contrae todos los botones expandibles"""
        self.tmrContraerPacientes.start()
        self.tmrContraerInformes.start()
        self.tmrContraerNotas.start()
        self.tmrContraerNosotros.start()
        self.tmrContraerSalir.start()
        self.tmrContraerUsuarios.start()        

    def teclaPresionadaEvent(self, event):
        """Evento al presionar teclas"""
        if event.key() == Qt.Key_Escape:
            self.clickBtnSalir()

    def softIn(self):
        """Muestra suavemente la ventana"""
        opacidad = self.windowOpacity()
        if not ventana_presentacion_.tmrSoftIn.isActive(
        ) and not ventana_presentacion_.tmrSoftOut.isActive(
        ) and not ventana_presentacion_.logo_.tmrSoftOut.isActive():
            opacidad += self.VELOCIDAD_OPACIDAD
        self.setWindowOpacity(opacidad)
        if self.windowOpacity() >= 1:
            self.tmrSoftIn.stop()
            #self.ventana_acceso_.ingresar(self.tmrSoftOut, self.VELOCIDAD_EXPANSION)
            self.ventana_cambio_contrasenia_.show()

    def softOut(self):
        """Desaparece suavemente la ventana y cierra la aplicación"""
        opacidad = self.windowOpacity()
        opacidad -= self.VELOCIDAD_OPACIDAD
        self.setWindowOpacity(opacidad)
        if self.windowOpacity() <= 0:
            app.closeAllWindows()
            app.quit()




    #Métodos de expansión y contracción de los botones
    def expandirBtnSalir(self):
        """Expande el botón de salir"""
        btnSalir_x = self.btnSalirDesplegable.x()
        btnSalir_y = self.btnSalirDesplegable.y()
        btnSalir_ancho = self.btnSalirDesplegable.width()
        btnSalir_alto = self.btnSalirDesplegable.height()
        if btnSalir_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnSalir_ancho = self.btnSalirDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnSalirDesplegable.setGeometry(
                btnSalir_x, btnSalir_y, btnSalir_ancho, btnSalir_alto)
        if self.btnSalirDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirSalir.stop()

    def contraerBtnSalir(self):
        """Contrae el botón de salir"""
        btnSalir_x = self.btnSalirDesplegable.x()
        btnSalir_y = self.btnSalirDesplegable.y()
        btnSalir_ancho = self.btnSalirDesplegable.width()
        btnSalir_alto = self.btnSalirDesplegable.height()
        if btnSalir_ancho > int(self.ancho_pantalla * 70 / 1920):
            btnSalir_ancho = self.btnSalirDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnSalirDesplegable.setGeometry(
                btnSalir_x, btnSalir_y, btnSalir_ancho, btnSalir_alto)
        if self.btnSalirDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerSalir.stop()

    def expandirBtnUsuarios(self):
        """Expande el botón de usuarios"""
        btnUsuarios_x = self.btnUsuariosDesplegable.x()
        btnUsuarios_y = self.btnUsuariosDesplegable.y()
        btnUsuarios_ancho = self.btnUsuariosDesplegable.width()
        btnUsuarios_alto = self.btnUsuariosDesplegable.height()
        if btnUsuarios_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnUsuarios_ancho = self.btnUsuariosDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnUsuariosDesplegable.setGeometry(btnUsuarios_x, btnUsuarios_y, btnUsuarios_ancho, btnUsuarios_alto)
        if self.btnUsuariosDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirUsuarios.stop()

    def contraerBtnUsuarios(self):
        """Contrae el botón de usuarios"""
        btnUsuarios_x = self.btnUsuariosDesplegable.x()
        btnUsuarios_y = self.btnUsuariosDesplegable.y()
        btnUsuarios_ancho = self.btnUsuariosDesplegable.width()
        btnUsuarios_alto = self.btnUsuariosDesplegable.height()
        if self.btnUsuariosDesplegable.width() > int(self.ancho_pantalla * 70 / 1920):
            btnUsuarios_ancho = self.btnUsuariosDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnUsuariosDesplegable.setGeometry(btnUsuarios_x, btnUsuarios_y, btnUsuarios_ancho, btnUsuarios_alto)
        if self.btnUsuariosDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerUsuarios.stop()

    def expandirBtnPacientes(self):
        """Expande el botón de pacientes"""
        btnPacientes_x = self.btnPacientesDesplegable.x()
        btnPacientes_y = self.btnPacientesDesplegable.y()
        btnPacientes_ancho = self.btnPacientesDesplegable.width()
        btnPacientes_alto = self.btnPacientesDesplegable.height()
        if btnPacientes_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnPacientes_ancho = self.btnPacientesDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnPacientesDesplegable.setGeometry(
                btnPacientes_x, btnPacientes_y, btnPacientes_ancho, btnPacientes_alto)
        if self.btnPacientesDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirPacientes.stop()

    def contraerBtnPacientes(self):
        """Contrae el botón de pacientes"""
        btnPacientes_x = self.btnPacientesDesplegable.x()
        btnPacientes_y = self.btnPacientesDesplegable.y()
        btnPacientes_ancho = self.btnPacientesDesplegable.width()
        btnPacientes_alto = self.btnPacientesDesplegable.height()
        if self.btnPacientesDesplegable.width() > int(self.ancho_pantalla * 70 / 1920):
            btnPacientes_ancho = self.btnPacientesDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnPacientesDesplegable.setGeometry(
                btnPacientes_x, btnPacientes_y, btnPacientes_ancho, btnPacientes_alto)
        if self.btnPacientesDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerPacientes.stop()

    def expandirBtnInformes(self):
        """Expande el botón de informes"""
        btnInformes_x = self.btnInformesDesplegable.x()
        btnInformes_y = self.btnInformesDesplegable.y()
        btnInformes_ancho = self.btnInformesDesplegable.width()
        btnInformes_alto = self.btnInformesDesplegable.height()
        if btnInformes_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnInformes_ancho = self.btnInformesDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnInformesDesplegable.setGeometry(
                btnInformes_x, btnInformes_y, btnInformes_ancho, btnInformes_alto)
        if self.btnInformesDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirInformes.stop()

    def contraerBtnInformes(self):
        """Contrae el botón de informes"""
        btnInformes_x = self.btnInformesDesplegable.x()
        btnInformes_y = self.btnInformesDesplegable.y()
        btnInformes_ancho = self.btnInformesDesplegable.width()
        btnInformes_alto = self.btnInformesDesplegable.height()
        if self.btnInformesDesplegable.width() > int(self.ancho_pantalla * 70 / 1920):
            btnInformes_ancho = self.btnInformesDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnInformesDesplegable.setGeometry(
                btnInformes_x, btnInformes_y, btnInformes_ancho, btnInformes_alto)
        if self.btnInformesDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerInformes.stop()

    def expandirBtnNotas(self):
        """Expande el botón de notas"""
        btnNotas_x = self.btnNotasDesplegable.x()
        btnNotas_y = self.btnNotasDesplegable.y()
        btnNotas_ancho = self.btnNotasDesplegable.width()
        btnNotas_alto = self.btnNotasDesplegable.height()
        if btnNotas_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnNotas_ancho = self.btnNotasDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnNotasDesplegable.setGeometry(
                btnNotas_x, btnNotas_y, btnNotas_ancho, btnNotas_alto)
        if self.btnNotasDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirNotas.stop()

    def contraerBtnNotas(self):
        """Contrae el botón de notas"""
        btnNotas_x = self.btnNotasDesplegable.x()
        btnNotas_y = self.btnNotasDesplegable.y()
        btnNotas_ancho = self.btnNotasDesplegable.width()
        btnNotas_alto = self.btnNotasDesplegable.height()
        if self.btnNotasDesplegable.width() > int(self.ancho_pantalla * 70 / 1920):
            btnNotas_ancho = self.btnNotasDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnNotasDesplegable.setGeometry(
                btnNotas_x, btnNotas_y, btnNotas_ancho, btnNotas_alto)
        if self.btnNotasDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerNotas.stop()

    def expandirBtnNosotros(self):
        """Expande el botón de nosotros"""
        btnNosotros_x = self.btnNosotrosDesplegable.x()
        btnNosotros_y = self.btnNosotrosDesplegable.y()
        btnNosotros_ancho = self.btnNosotrosDesplegable.width()
        btnNosotros_alto = self.btnNosotrosDesplegable.height()
        if btnNosotros_ancho < int(self.ancho_pantalla * 300 / 1920):
            btnNosotros_ancho = self.btnNosotrosDesplegable.width() + self.VELOCIDAD_EXPANSION
            self.btnNosotrosDesplegable.setGeometry(
                btnNosotros_x, btnNosotros_y, btnNosotros_ancho, btnNosotros_alto)
        if self.btnNosotrosDesplegable.width() == int(self.ancho_pantalla * 300 / 1920):
            self.tmrExpandirNosotros.stop()

    def contraerBtnNosotros(self):
        """Contrae el botón de nosotros"""
        btnNosotros_x = self.btnNosotrosDesplegable.x()
        btnNosotros_y = self.btnNosotrosDesplegable.y()
        btnNosotros_ancho = self.btnNosotrosDesplegable.width()
        btnNosotros_alto = self.btnNosotrosDesplegable.height()
        if self.btnNosotrosDesplegable.width() > int(self.ancho_pantalla * 70 / 1920):
            btnNosotros_ancho = self.btnNosotrosDesplegable.width() - self.VELOCIDAD_EXPANSION
            self.btnNosotrosDesplegable.setGeometry(
                btnNosotros_x, btnNosotros_y, btnNosotros_ancho, btnNosotros_alto)
        if self.btnNosotrosDesplegable.width() == int(self.ancho_pantalla * 70 / 1920):
            self.tmrContraerNosotros.stop()





if __name__ == "__main__":
    #Instancias
    app = QApplication(sys.argv)
    ventana_principal_ = ventanaPrincipal()
    ventana_presentacion_ = VentanaPresentacion()
    #Cerramos las ventanas que no queremos que se vean al inicio
    ventana_principal_.ventana_cambio_contrasenia_.close()
    ventana_principal_. ventana_acceso_.close()
    #Presentación
    ventana_presentacion_.show()
    ventana_presentacion_.tmrSoftIn.start()
    # Cargamos la fecha y hora antes de que se muestren
    mostrarFechaHora(ventana_principal_.lblFecha, ventana_principal_.lcdHora)
    ventana_principal_.tmrFechaHora.start()
    #Mostramos la interfaz principal
    ventana_principal_.show()
    ventana_principal_.tmrSoftIn.start()
    #Iniciamos la aplicacióni
    #sys.exit(app.exec_())
    app.exec_()
    del(app)
