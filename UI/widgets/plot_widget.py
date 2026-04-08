import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout

class BiorreactorPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0) #Quitamos márgenes para un diseño limpio

        #1. Creamos el lienzo del gráfico
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.showGrid(x=True, y=True, alpha=0.3)
        self.plot_graph.addLegend() #Agrega la leyebda automáticamente

        layout.addWidget(self.plot_graph)

        #2. Pre creamos las líneas vacías
        self.curve_x = self.plot_graph.plot([], [], name="Biomasa (X)")
        self.curve_s = self.plot_graph.plot([], [], name="Sustrato (S)")
        #self.curve_x = self.plot_graph.plot([], [], pen=pg.mkPen('#a6e3a1', width=3), name="Biomasa (X)") #Catppuccin Green
        #self.curve_s = self.plot_graph.plot([], [], pen=pg.mkPen('#f38ba8', width=3), name="Sustrato (S)") #Catppuccin Red

        #3. Para forzar un tema por defecto
        self.aplicar_tema_grafica(modo_oscuro=True)

    def update_plot(self, t, X, S):
        """Esta función inyecta los nuevos arreglos de SciPy en las líneas dibujadas"""
        self.curve_x.setData(t, X)
        self.curve_s.setData(t, S)

    def aplicar_tema_grafica(self, modo_oscuro=True):
        """Cambia los colores del fondo, los ejes y las líneas según el tema"""

        #Definición de los colores
        if modo_oscuro:
            #Tema Catpuccin Mocha
            color_fondo = '#1e1e2e' #Mocha Base
            color_texto = '#cdd6f4' #Text
            color_biomasa = '#a6e3a1' #Green
            color_sustrato = '#f38ba8' #Rojo
        else:
            #Tema Light Latte
            color_fondo = '#eff1f5' #Latte Base
            color_texto = '#4c4f69' #Latte Text
            color_biomasa = '#40a02b' #Latte Green
            color_sustrato = '#d20f39' #Latte Red
        
        #Poner el color al fondo
        self.plot_graph.setBackground(color_fondo)

        #Títulos y textos
        self.plot_graph.setTitle("Cinética de crecimiento (Modelo de Monod)", color=color_texto, size="12pt")
        
        eje_izq = self.plot_graph.getAxis('left')
        eje_inf = self.plot_graph.getAxis('bottom')

        #Actualizamos las etiquetas de los ejes
        eje_izq.setLabel('Concentración', units='g/L', color=color_texto)
        eje_inf.setLabel('Tiempo', units='h', color=color_texto)

        #Cambiamos el color de los números y las rayas.
        eje_izq.setPen(color_texto)
        eje_izq.setTextPen(color_texto)
        eje_inf.setPen(color_texto)
        eje_inf.setTextPen(color_texto)

        #Cambiamos el color de las curvas (si ya existen)
        self.curve_x.setPen(pg.mkPen(color_biomasa, width=3))
        self.curve_s.setPen(pg.mkPen(color_sustrato, width=3))

        #Leyenda
        #PyQtGraph guarda los textos de la leyenda en una lista, se debe iterar para cambiar el color
        if self.plot_graph.plotItem.legend:
            for sample, label in self.plot_graph.plotItem.legend.items:
                label.setText(label.text, color=color_texto)

