from services.threads import SimulationThread

class MainController:
    def __init__(self, view):
        self.view = view

        #1. Conectamos la señal de la UI al método de este controlador 
        self.view.simulate_requested.connect(self.run_simulation)

        self.tread = None #Aquí guardaremos el hilo temporalmente

    def run_simulation(self, datos_ui):
        """Se activa cuando el usuario presiona el botón de la UI"""
        print("\n[Controlador] Iniciando simulación en segundo plano")

        #Desactivamos el botón visualmente para que el usuario no le de varias veces seguidas
        self.view.btn_simulate.setEnabled(False)
        self.view.btn_simulate.setText("Calculando...")

        #2. Creamos el hilo y le pasamos los datos
        self.thread = SimulationThread(datos_ui)

        #3. Conectamos la señal de "terminé" del hilo a nuestro método receptor
        self.thread.finished_signal.connect(self.on_simulation_finished)

        #4. Arrancamos el hilo
        self.thread.start()

    def on_simulation_finished(self, t, X, S):
        """Se activa cuando SciPy termina de integrar las ecuaciones"""
        print("[Controlador] Simulación terminada con éxito")

        #Reactovamos el botón en la interfaz
        self.view.btn_simulate.setEnabled(True)
        self.view.btn_simulate.setText("Ejecutar Simulación")

        self.view.plot_widget.update_plot(t, X, S)