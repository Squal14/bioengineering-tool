import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Qt 

#Se debe asegurar que python esté corriendo en la carpeta del proyecto. 

from UI.views.kinetics_view import KineticsInputView
from controllers.main_controller import MainController


class BioreactorSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Se configura la ventana principal
        self.setWindowTitle("Simulador de biorreactor")
        self.resize(1400, 600) #Ancho y alto inicial

        #1. Instanciamos nuestra vista de cinéticas
        self.vista_cinetica = KineticsInputView()

        #2. Establecemos como el componente central de esta ventana
        self.setCentralWidget(self.vista_cinetica)

        #3. Conectamos la señal. 
        #En realidad debe estar conectado al controlador.
        self.controlador = MainController(self.vista_cinetica)

    def prueba_recepcion_datos(self, datos):

        """Esta función solo es para verificar que el botón y la señal funcionan"""
        print("\n--- Señal recibida en main ---")
        print("Datos listos para enviar a SciPy:")
        for clave, valor in datos.items():
            print(f"{clave}: {valor}")
        print("--------------------------------\n")


def aplicar_tema_sistema(app, ventana=None):
        """Detectamos el tema de Windows y cargar el archivo QSS correspondiente"""
        #1. Leer el esquema de color del sistema operativo
        esquema_sistema = app.styleHints().colorScheme()
        modo_oscuro = (esquema_sistema == Qt.ColorScheme.Dark)

        #2. Elegimos la ruta del archivo
        if esquema_sistema == Qt.ColorScheme.Dark:
            ruta_qss = "assets/themes/dark_mocha.qss"
            print("[Tema] Widnows está en modo oscuro. Aplicando Catpuccin Mocha.")
        else:
            ruta_qss = "assets/themes/light_latte.qss"
            print("[Tema] Windows está en modo claro. Aplicando Catpuccin Latte.")
        
        #3. Leemos el arcvhivo y lo aplicamos.
        try:
            with open(ruta_qss, "r", encoding="utf-8") as archivo:
                app.setStyleSheet(archivo.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema en {ruta_qss}")

        #Le avisamos a la gráfica que cambie sus colores
        if ventana is not None:
            ventana.vista_cinetica.plot_widget.aplicar_tema_grafica(modo_oscuro)

if __name__=="__main__":

    #Creamos la aplicación base
    app = QApplication(sys.argv)

    #Creamos y mostramos la ventana principal
    ventana = BioreactorSimulatorApp()
    
    #Aplicamos el tema la primera vez que se abre la app.
    aplicar_tema_sistema(app, ventana)
    #Conectamos una señal para saber el tema de Windows en tiempo real. 
    app.styleHints().colorSchemeChanged.connect(lambda: aplicar_tema_sistema(app, ventana))
    
    ventana.show()

    #Arrancamos el ciclo de la aplicación.
    sys.exit(app.exec())