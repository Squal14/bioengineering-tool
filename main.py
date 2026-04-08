import sys
from PySide6.QtWidgets import QApplication, QMainWindow

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

if __name__=="__main__":
    #Se crea la hoja de estilo catppuccin mocha(QSS)
    estilo_catppuccin_mocha = """
        /* 1. EL FONDO DE LA INTERFAZ (Aplica a todas las ventanas) */
        QWidget {
            background-color: #1e1e2e; /* Base */
            color: #cdd6f4;            /* Text */
            font-size: 12pt;           /* Tamaño de letra un poco más grande */
        }

        /* 2. EL ESTILO DE LOS BOTONES */
        QPushButton {
            background-color: #181825; /* Mantle */
            color: #cdd6f4;              /* Text */
            border: none;              /* Sin borde feo por defecto */
            border-radius: 6px;        /* Bordes suavemente redondeados */
            padding: 10px 20px;        /* Botón más alto y ancho */
            font-weight: bold;         /* Letra negrita */
        }

        /* 3. EFECTO AL PASAR EL RATÓN (Hover) */
        QPushButton:hover {
            background-color: #45475a; /* Surface 1 */
        }

        /* 4. EFECTO AL HACER CLIC (Pressed) */
        QPushButton:pressed {
            background-color: #11111b; /* Crust */
        }

        /* 5. LAS CAJAS DE NÚMEROS (Para que hagan juego) */
        QDoubleSpinBox {
            background-color: #181825; /* Mantle */
            border: 1px solid #cba6f7; /* Mauve */
            border-radius: 12px;
            padding: 5px;
            padding-right: 25px;
        }
        
        /* 6. Estilizar el contenedor */
        QGroupBox {
            border: 1px solid #cdd6f4; /* Text */
            border-radius: 15px; /* Bordes redondeados */
            margin-top: 14px; /* Da espacio arriba para que entre el título */
        }

        /* 7. Estilizar el título del contenedor */
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: margin;
            left: 0px; /* Lo empuja un poco a la derecha */
            padding: 0 5px; /* Un pequeño margen alrededor del texto */
            color: #cdd6f4; /* Text */
            font-weight: bold
        }

        /* 8. Estilizar los textos (Etiquetas) */
        QLabel {
            color: #cdd6f4 /* Text */
        }
    """

    #Creamos la aplicación base
    app = QApplication(sys.argv)

    #Aplicamos un estilo base un poco más limpio que el de Windows por defecto.
    app.setStyleSheet(estilo_catppuccin_mocha)
    
    #Creamos y mostramos la ventana principal
    ventana = BioreactorSimulatorApp()
    ventana.show()

    #Arrancamos el ciclo de la aplicación.
    sys.exit(app.exec())