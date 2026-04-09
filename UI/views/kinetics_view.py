from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QDoubleSpinBox, QPushButton, QGroupBox, QHBoxLayout, QComboBox)
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

        #==================SUBMENÚ============================
        group_modelo = QGroupBox("Selección de Modelo")
        layout_modelo = QVBoxLayout()

        self.combo_modelo = QComboBox()
        self.combo_modelo.addItems(["Modelo de Monod", "Luedeking-Piret"])
        #SE CONECTA EL CAMBIO DE TEXTO A UNA FUNCIÓN
        self.combo_modelo.currentTextChanged.connect(self.on_model_changed)

        layout_modelo.addWidget(self.combo_modelo)
        group_modelo.setLayout(layout_modelo)
        left_panel.addWidget(group_modelo)

        #=========NUEVAMENTE PANEL IZQUIERDO===============
        #Marco y título.
        group_box = QGroupBox("Parámetros del cultivo")
        #Formulario para obtener los datos.
        form_layout = QFormLayout()

        #PARÁMETROS MONOD.
        self.input_x0 = self.create_spinbox(min_val=0.0000001, max_val=1000.0, default=0.1)
        self.input_s0 = self.create_spinbox(min_val=0.0, max_val=5000.0, default=20.0)
        self.input_mumax = self.create_spinbox(min_val=0.0001, max_val=8.0, default=0.5)
        self.input_ks = self.create_spinbox(min_val=0.0001, max_val=100.0, default=2.0)

        #Ahora las filas al formulario
        form_layout.addRow("Biomasa inicial (X0) [g/L]:", self.input_x0)
        form_layout.addRow("Sustrato inicial (S0) [g/L]:", self.input_s0)
        form_layout.addRow("Velocidad específica de crecimiento máxima (μmax) [1/h]:", self.input_mumax)
        form_layout.addRow("Constante de saturación (Ks) [g/L]:", self.input_ks)

        group_box.setLayout(form_layout)
        left_panel.addWidget(group_box)

        #PARÁMETROS LUEDEKING PIRET (EXTRA)
        self.group_lp = QGroupBox("Formación de Producto")
        form_lp = QFormLayout()

        self.input_p0 = self.create_spinbox(min_val=0.0000001, max_val=1000.0, default=0.0)
        self.input_alfa = self.create_spinbox(min_val=0.0, max_val=10.0, default=0.1)
        self.input_beta = self.create_spinbox(min_val=0.0, max_val=10.0, default=0.05)
        self.input_yxs = self.create_spinbox(min_val=0.0001, max_val=10.0, default=0.5)
        
        form_lp.addRow("Producto inicial (P0) [g/L]", self.input_p0)
        form_lp.addRow("Asociado al crecimiento (α) [g/L]", self.input_alfa)
        form_lp.addRow("No asociado (β) [g/L]", self.input_beta)
        form_lp.addRow("Rendimiento (Yxs) [g/L]", self.input_yxs)

        self.group_lp.setLayout(form_lp)
        self.group_lp.setVisible(False) #Oculto por defecto
        left_panel.addWidget(self.group_lp)

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
    
    def on_model_changed(self, texto):
        """Muestra u oculta los parámetros de Luedeking-Piret"""
        if texto == "Luedeking-Piret":
            self.group_lp.setVisible(True)
        else:
            self.group_lp.setVisible(False)
    
    def on_simulate_clicked(self):
        """Esta función se ejecuta al presionar el botón"""
        modelo_actual = self.combo_modelo.currentText()
        #1. Recolectamos los valores limpios y seguros
        datos = {
            "modelo": modelo_actual,
            "X0": self.input_x0.value(),
            "S0": self.input_s0.value(),
            "mu_max": self.input_mumax.value(),
            "Ks": self.input_ks.value()
        }

        if modelo_actual == "Luedeking-Piret":
            datos["P0"] = self.input_p0.value()
            datos["alfa"] = self.input_alfa.value()
            datos["beta"] = self.input_beta.value()
            datos["Yxs"] = self.input_yxs.value()
        #2. Emitimos la señal con el diccionario
        #El controlador (en controllers/main_controller.py) estará escuchando esto.
        self.simulate_requested.emit(datos)