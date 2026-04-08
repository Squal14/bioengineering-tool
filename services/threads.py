import numpy as np
from PySide6.QtCore import QThread, Signal
from services.solvers import resolver_biorreactor

class SimulationThread(QThread):
    #Definimos la señal que enviará lo sresultados: 3 arreglos de Numpy (tiempo, biomasa, sustrato)
    finished_signal = Signal(np.ndarray, np.ndarray, np.ndarray)

    def __init__(self, datos_ui):
        super().__init__()
        self.datos_ui = datos_ui
    
    def run(self):
        #Todo lo que esté dentro de run() ocurre en segundo plano
        #Llamamos a nuestra función SciPy
        t, X, S = resolver_biorreactor(self.datos_ui)

        #Cuando termina, emitimos los vectores resultantes
        self.finished_signal.emit(t, X, S)
