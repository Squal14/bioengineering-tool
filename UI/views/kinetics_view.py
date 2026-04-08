from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QDoubleSpinBox, QPushButton, QGroupBox, QHBoxLayout)
from PySide6.QtCore import Signal
from UI.widgets.plot_widget import BiorreactorPlotWidget 

class KineticsInputView(QWidget):

    #Primero se usa una señal para poder saber que se van a ingresar los datos.
    simulate_requested = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        #Layout principal dividido
        main_layout = QHBoxLayout(self)

        #=============PANEL IZQUIERDO (CONTROLES) ===============
        left_panel = QVBoxLayout(self)
        #Marco y título.
        group_box = QGroupBox("Parámetros del cultivo")
        #Formulario para obtener los datos.
        form_layout = QFormLayout()

        #Ahora vienen las entradas con valores mínimos, máximos y predeterminados.
        self.input_x0 = self.create_spinbox(min_val=0.001, max_val=100.0, default=0.1)
        self.input_s0 = self.create_spinbox(min_val=0.0, max_val=500.0, default=20.0)
        self.input_mumax = self.create_spinbox(min_val=0.001, max_val=5.0, default=0.5)
        self.input_ks = self.create_spinbox(min_val=0.001, max_val=100.0, default=2.0)

        #Ahora las filas al formulario
        form_layout.addRow("Biomasa inicial (X0) [g/L]:", self.input_x0)
        form_layout.addRow("Sustrato inicial (S0) [g/L]:", self.input_s0)
        form_layout.addRow("Velocidad específica de crecimiento máxima (μmax) [1/h]:", self.input_mumax)
        form_layout.addRow("Constante de saturación (Ks) [g/L]:", self.input_ks)

        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        #Botón de acción principal
        self.btn_simulate = QPushButton("Ejecutar simulación")
        #Se conecta el click al botón principal
        self.btn_simulate.clicked.connect(self.on_simulate_clicked)

        left_panel.addWidget(self.btn_simulate)
        left_panel.addStretch() #Empuja los controles hacia arriba

        # =========PANEL DERECHO (GRÁFICO)============
        self.plot_widget = BiorreactorPlotWidget()

        # ===== UNIMOS LOS PANELES ================
        #Le damos proporción 1 al panel de control y 3 al gráfico 
        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addWidget(self.plot_widget, stretch=3)

    def create_spinbox(self, min_val, max_val, default):
        """Función auxiliar para configurar rápidamente las cajas de números"""
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val) #Evita que el usuario ingrese datos fuera de los valores min y max.
        spinbox.setValue(default)
        spinbox.setDecimals(3)
        return spinbox
    
    def on_simulate_clicked(self):
        """Esta función se ejecuta al presionar el botón"""
        #1. Recolectamos los valores limpios y seguros
        datos_cineticos = {
            "X0": self.input_x0.value(),
            "S0": self.input_s0.value(),
            "mu_max": self.input_mumax.value(),
            "Ks": self.input_ks.value()
        }

        #2. Emitimos la señal con el diccionario
        #El controlador (en controllers/main_controller.py) estará escuchando esto.
        self.simulate_requested.emit(datos_cineticos)