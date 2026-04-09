import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Qt 

#Se debe asegurar que python esté corriendo en la carpeta del proyecto. 

from UI.views.kinetics_view import KineticsInputView
from controllers.main_controller import MainController


class BioreactorSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Se configura la ventana principal
        self.setWindowTitle("Herramienta de Ingeniería Biotecnológica")
        self.resize(1400, 650) #Ancho y alto inicial


        #===========LAYOUT PRINCIPAL DIVIDIDO EN DOS=================
        widget_central = QWidget()
        #Establecemos como el componente central de esta ventana
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0) #Sin espacio entre el menú y el contenido

        #BARRA LATERAL (Menú Principal)
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar") #Identificador para el QSS.
        self.sidebar.setFixedWidth(260)
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(15, 25, 15, 20)

        #TÍTULO Y LOGO
        self.lbl_logo = QLabel("⚙️ BioSim Pro")
        self.lbl_logo.setObjectName("LogoText")
        layout_sidebar.addWidget(self.lbl_logo)
        layout_sidebar.addSpacing(30)

        #BOTÓN 1: CINÉTICAS (Activo)
        self.btn_cineticas = QPushButton("Cinéticas de crecimiento celular")
        self.btn_cineticas.setObjectName("MenuButton")
        self.btn_cineticas.setCheckable(True)
        self.btn_cineticas.setChecked(True) #Empieza seleccionado

        #BOTÓN 2: DISEÑO DE BIORREACTOR
        self.btn_reactores = QPushButton("Diseño de biorreactores")
        self.btn_reactores.setObjectName("MenuButton")
        self.btn_reactores.setCheckable(True)
        self.btn_reactores.setChecked(False)

        layout_sidebar.addWidget(self.btn_cineticas)
        layout_sidebar.addWidget(self.btn_reactores)
        layout_sidebar.addStretch() #Empuja los botones hacia arriba

        #================ÁREA DE TRABAJO=======================
        self.contenedor_pantallas = QStackedWidget()

        #SE CREA LA VISTA Y SE INTRODUCE AL MAZO
        self.vista_cinetica = KineticsInputView()
        self.contenedor_pantallas.addWidget(self.vista_cinetica)

        #SE ENSAMBLA TOD0
        layout_principal.addWidget(self.sidebar)
        layout_principal.addWidget(self.contenedor_pantallas)

        #INICIAMOS EL CONTROLADOR PASÁNDOLE LA VISTA
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