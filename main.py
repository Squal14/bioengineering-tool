import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

#Se debe asegurar que python esté corriendo en la carpeta del proyecto. 

from UI.views.kinetics_view import KineticsInputView
from controllers.main_controller import MainController


class BioreactorSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #Se configura la ventana principal
        self.setWindowTitle("Herramienta de Ingeniería Biotecnológica")
        self.resize(1400, 650) #Ancho y alto inicial


        #===========LAYOUT PRINCIPAL=================
        widget_central = QWidget()
        #Establecemos como el componente central de esta ventana
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0) #Sin espacio entre el menú y el contenido

        #BARRA LATERAL (Menú Principal)
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar") #Identificador para el QSS.
        self.sidebar.setFixedWidth(285)
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(15, 25, 15, 20)

        #TÍTULO GENERAL, BOTÓN TOGGLE Y LOGO
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0 ,0 ,0)

        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setObjectName("ToggleButton")
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        self.lbl_logo = QLabel("BioSim Pro")
        self.lbl_logo.setObjectName("LogoText")
        
        header_layout.addWidget(self.btn_toggle)
        header_layout.addWidget(self.lbl_logo)
        header_layout.addStretch()        
        
        layout_sidebar.addLayout(header_layout)
        layout_sidebar.addSpacing(30)

        #BOTÓN 1: CINÉTICAS (Activo)
        self.btn_cineticas = QPushButton("📈 Cinéticas de crecimiento celular")
        self.btn_cineticas.setObjectName("MenuButton")
        self.btn_cineticas.setCheckable(True)
        self.btn_cineticas.setChecked(True) #Empieza seleccionado

        #BOTÓN 2: DISEÑO DE BIORREACTOR
        self.btn_reactores = QPushButton("🧪 Diseño de biorreactores")
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

    def toggle_sidebar(self):
        #MEDIDAS DE LA BARRA
        ancho_expandido = 285
        ancho_colapsado = 70

        ancho_actual = self.sidebar.width()
        if ancho_actual > 100:
            nuevo_ancho = ancho_colapsado
            self.lbl_logo.hide() #Se oculta el texto

            self.btn_cineticas.setText("📈")
            self.btn_reactores.setText("🧪")
        else:
            nuevo_ancho = ancho_expandido
            self.lbl_logo.show() #Se muestra el texto

            self.btn_cineticas.setText("📈 Cineticas de crecimiento celular")
            self.btn_reactores.setText("🧪 Diseño de biorreactores")

        #ANIMACIÓN PRINCIPAL
        #SE GUARDAN EN SELF PARA QUE NO SE BORRE EN LA MEMORIA
        self.animacion1 = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animacion1.setDuration(250) #En ms
        self.animacion1.setStartValue(ancho_actual)
        self.animacion1.setEndValue(nuevo_ancho)
        self.animacion1.setEasingCurve(QEasingCurve.InOutQuad) #Movimiento suave

        self.animacion2 = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.animacion2.setDuration(250) #En ms
        self.animacion2.setStartValue(ancho_actual)
        self.animacion2.setEndValue(nuevo_ancho)
        self.animacion2.setEasingCurve(QEasingCurve.InOutQuad) #Movimiento suave

        self.animacion1.start()
        self.animacion2.start()

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