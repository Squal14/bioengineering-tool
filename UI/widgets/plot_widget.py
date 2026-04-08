import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout

class BiorreactorPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0) #Quitamos márgenes para un diseño limpio

        #1. Configuración global para que se vea elegante (Tema oscuro)
        pg.setConfigOption('background', '#1e1e2e') #Base
        pg.setConfigOption('foreground', '#cdd6f4') #Text

        #2. Creamos el lienzo del gráfico
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setTitle("Cinética de crecimiento (Modelo de Monod)")
        self.plot_graph.setLabel('left', 'Concentración', units='g/L')
        self.plot_graph.setLabel('bottom', 'Tiempo', units='h')
        self.plot_graph.showGrid(x=True, y=True, alpha=0.3)
        self.plot_graph.addLegend() #Agrega la leyebda automáticamente

        layout.addWidget(self.plot_graph)

        #3. Pre creamos las líneas vacías
        #'g' es verde para biomasa, '#ff007f' es rosa neón para sustrato
        self.curve_x = self.plot_graph.plot([], [], pen=pg.mkPen('g', width=3), name="Biomasa (X)")
        self.curve_s = self.plot_graph.plot([], [], pen=pg.mkPen('#ff007f', width=3), name="Sustrato (S)")

    def update_plot(self, t, X, S):
        """Esta función inyecta los nuevos arreglos de SciPy en las líneas dibujadas"""
        self.curve_x.setData(t, X)
        self.curve_s.setData(t, S)
