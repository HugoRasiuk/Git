""" Datos globales """

#Programa para preparar las interfaces y los recursos.
#Pyprepare, el cual se debe ejecutar en el directorio del proyecto.

#Sintaxis para hacer el ejecutable
#pyinstaller --onefile --windowed --icon archivo.ico archivo_principal.py

#Para hacer backup de las bases de datos seleccionar "Custom", utilizar
#el nombre de la base de datos con la extensión ".backup" y el 
#formato que sea backup. La extensión backup se pone por defecto al seleccionar backup.

#Cadena de conexión a la base de datos
CNXSTR = "host=localhost port=5432 dbname=agenda user=postgres password=her301272"

# Velocidad de movimiento de las ventanas
# Debe ser un número que al usarlo para dividir el
# número 200, su modulo  sea 0
VELOCIDAD_ANIMACION = 20

#Velocidad de incremento y decremento de la opacidad de las ventanas
VELOCIDAD_OPACIDAD = 0.01

#Velocidad de expansión de widgets a la hora de agrandarlos o achicarlos
VELOCIDAD_EXPANSION = 1
