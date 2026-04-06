import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

# 1. Crear la aplicación base
app = QApplication(sys.argv)

# 2. Crear una ventana simple
ventana = QWidget()
ventana.setWindowTitle("Prueba de PySide6")
ventana.resize(300, 150)

# 3. Agregar un texto
layout = QVBoxLayout()
etiqueta = QLabel("¡PySide6 está instalado y funcionando correctamente!")
layout.addWidget(etiqueta)
ventana.setLayout(layout)

# 4. Mostrar la ventana y arrancar el ciclo de la app
ventana.show()
sys.exit(app.exec())